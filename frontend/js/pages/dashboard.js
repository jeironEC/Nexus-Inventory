// Lógica principal del Dashboard

import { serviceProvider } from '../services/ServiceProvider.js';
import { authService } from '../services/AuthService.js';
import { reportService } from '../services/ReportService.js';
import { create, clearChildren } from '../utils/dom.js';
import { initTablePagination } from '../utils/base_page.js';
import { formatCurrency, formatNumber, updateKPIs } from '../utils/helpers.js';

// Inicializa la página del dashboard
export async function initDashboard() {
    if (!authService.isAuthenticated()) {
        window.location.href = '/index.html';
        return;
    }

    if (window.sidebar) window.sidebar.init('dashboard.html');
    if (window.pageHeader) window.pageHeader.init('Dashboard');

    await loadDashboardData();
}

// Carga todos los datos del dashboard concurrentemente
async function loadDashboardData() {
    try {
        await Promise.all([
            loadDashboardStatistics(),
            loadLowStockProductsTable(),
            loadRecentSales()
        ]);
    } catch (error) {
    }
}

// Carga y calcula las estadísticas del dashboard
async function loadDashboardStatistics() {
    try {
        const today = new Date().toISOString().split('T')[0];

        const [
            salesToday,
            purchasesToday,
            customersToday,
            lowStock
        ] = await Promise.all([
            fetchSalesTotal(today),
            fetchPurchasesTotal(today),
            fetchCustomersCount(today),
            reportService.getReportsInventoryLowStock()
        ]);

        const lowStockList = Array.isArray(lowStock.data) ? lowStock.data : (lowStock.data?.results || []);

        updateKPIs('.stats-grid', {
            total_revenue: salesToday,
            total_purchases: purchasesToday,
            low_stock_count: lowStockList.length,
            new_customers: customersToday
        }, {
            total_revenue: formatCurrency,
            total_purchases: formatCurrency,
            low_stock_count: formatNumber,
            new_customers: formatNumber
        });

    } catch (error) {
    }
}

// Obtiene el total de ventas de un día
async function fetchSalesTotal(date) {
    const res = await serviceProvider.sales.getAll({ date_from: date, date_to: date, state: 'COMPLETED', limit: 1000 });
    const data = res.data?.results || (Array.isArray(res.data) ? res.data : []);
    return data.reduce((sum, s) => sum + parseFloat(s.total_amount || 0), 0);
}

// Obtiene el total de compras de un día
async function fetchPurchasesTotal(date) {
    const res = await serviceProvider.purchases.getAll({ date_from: date, date_to: date, state: 'COMPLETED', limit: 1000 });
    const data = res.data?.results || (Array.isArray(res.data) ? res.data : []);
    return data.reduce((sum, p) => sum + parseFloat(p.total_amount || 0), 0);
}

// Obtiene el conteo de clientes de un día
async function fetchCustomersCount(date) {
    const res = await serviceProvider.customers.getAll({ date_from: date, date_to: date, limit: 1000 });
    const data = res.data?.results || (Array.isArray(res.data) ? res.data : []);
    return data.length;
}

// Carga productos con stock bajo para la tabla
async function loadLowStockProductsTable() {
    try {
        const response = await reportService.getReportsInventoryLowStock();
        if (response.success && response.data) {
            const productList = Array.isArray(response.data) ? response.data : (response.data.results || []);
            initTablePagination(productList, 25, renderLowStockTable, '#stock-pagination');
        }
    } catch (error) {
    }
}

// Carga las ventas recientes para la tabla
async function loadRecentSales() {
    try {
        const response = await serviceProvider.sales.getAll({ ordering: '-created_at', limit: 100 });
        if (response.success && response.data) {
            const saleList = Array.isArray(response.data) ? response.data : (response.data.results || []);
            initTablePagination(saleList, 25, renderRecentSalesTable, '#sales-pagination');
        }
    } catch (error) {
    }
}

// Renderiza las filas de ventas recientes
function renderRecentSalesTable(sales) {
    const tbody = document.getElementById('recent-sales-tbody');
    if (!tbody) return;

    clearChildren(tbody);

    sales.forEach(function renderSaleRow(sale) {
        const tr = create('tr');

        const customer = sale.customer || {};
        const customerName = customer.first_name ? `${customer.first_name} ${customer.last_name || ''}`.trim() : 'Cliente';

        tr.appendChild(create('td', '', {}, `#${sale.id}`));
        tr.appendChild(create('td', '', {}, customerName));
        tr.appendChild(create('td', '', {}, formatCurrency(sale.total_amount)));

        const badgeClass = sale.state === 'COMPLETED' ? 'badge-success' : 'badge-warning';
        const badgeText = sale.state === 'COMPLETED' ? 'OK' : 'Pte';
        const badgeTd = create('td');
        badgeTd.appendChild(create('span', `badge ${badgeClass}`, {}, badgeText));
        tr.appendChild(badgeTd);

        tbody.appendChild(tr);
    });
}

// Renderiza las filas de productos con stock bajo
function renderLowStockTable(products) {
    const tableBody = document.getElementById('low-stock-tbody');
    if (!tableBody) return;

    clearChildren(tableBody);

    products.forEach(function renderProductRow(product) {
        const tr = create('tr');

        tr.appendChild(create('td', '', {}, product.product_name || '-'));
        tr.appendChild(create('td', '', {}, product.category || '-'));
        tr.appendChild(create('td', '', {}, product.quantity.toString()));

        const badgeClass = product.quantity <= 3 ? 'badge-danger' : 'badge-warning';
        const badgeText = product.quantity <= 3 ? 'Crítico' : 'Bajo';
        const badgeTd = create('td');
        badgeTd.appendChild(create('span', `badge ${badgeClass}`, {}, badgeText));
        tr.appendChild(badgeTd);

        tableBody.appendChild(tr);
    });
}

document.addEventListener('DOMContentLoaded', initDashboard);
