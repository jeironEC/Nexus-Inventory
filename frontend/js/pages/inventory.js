// Lógica para la gestión de inventario

import { formatCurrency, formatDate, formatFullName } from '../utils/helpers.js';
import { Table } from '../components/Table.js';
import { toast } from '../components/Toast.js';
import { serviceProvider } from '../services/ServiceProvider.js';
import { getFilterValues, initFilterListeners, loadFilterSelects } from '../utils/filter_utils.js';
import { DEFAULT_PAGINATION_LIMIT } from '../utils/const.js';
import { TablePagination } from '../components/Pagination.js';
import { setupTableColumnToggles } from '../utils/base_page.js';

let inventoryTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (it) => `#${it.id}` },
    { label: 'Producto', type: 'primary', value: (it) => `<strong>${it.product?.name || 'Sin nombre'}</strong>` },
    { label: 'Categoría', type: 'normal', value: (it) => `<span class="badge" style="background: rgba(4, 85, 191, 0.1); color: var(--sky);">${it.product?.category?.name || 'General'}</span>` },
    {
        label: 'Stock Actual',
        type: 'normal',
        value: (it) => {
            const quantity = it.quantity || 0;
            const isLowStock = quantity > 0 && quantity < 10;
            const isOutStock = quantity === 0;
            return `
                <span class="badge ${isOutStock ? 'badge-danger' : (isLowStock ? 'badge-warning' : 'badge-success')}">
                    ${quantity} unidades
                </span>`;
        }
    },
    { label: 'P. Unitario', type: 'normal', value: (it) => formatCurrency(parseFloat(it.product?.sale_price || 0)) },
    { label: 'V. Total', type: 'normal', value: (it) => formatCurrency((it.quantity || 0) * parseFloat(it.product?.sale_price || 0)) },
    { label: 'Creado en', type: 'normal', value: (it) => it.created_at ? formatDate(it.created_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Actualizado en', type: 'normal', value: (it) => it.updated_at ? formatDate(it.updated_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Eliminado en', type: 'normal', value: (it) => it.deleted_at ? formatDate(it.deleted_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Creado por', type: 'audit', value: (it) => it.created_by?.first_name ? formatFullName(it.created_by) : (it.created_by?.email || '-') },
    { label: 'Actualizado por', type: 'audit', value: (it) => it.updated_by?.first_name ? formatFullName(it.updated_by) : (it.updated_by?.email || '-') },
    { label: 'Eliminado por', type: 'audit', value: (it) => it.deleted_by?.first_name ? formatFullName(it.deleted_by) : (it.deleted_by?.email || '-') }
];

// Inicializa la página de inventario
async function initInventoryPage() {
    if (window.sidebar) {
        window.sidebar.init('inventory.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Inventario');
    }

    inventoryTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
    });

    setupTableColumnToggles();

    await loadFilterSelects(['inventory-filter-product-id']);

    // Inicializar selects buscables en filtros
    import('../components/SearchableSelect.js').then(m => {
        m.SearchableSelect.initAll('.card-body');
    });

    await loadInventoryData();

    initFilterListeners('.card', async () => {
        await loadInventoryData();
    });
}

// Carga los datos del inventario
async function loadInventoryData() {
    inventoryTable.showLoading();

    try {
        const filters = { limit: 100, ...getFilterValues('.card') };

        const response = await serviceProvider.inventories.getAll(filters);
        if (response.success && response.data) {
            const items = response.data.results || (Array.isArray(response.data) ? response.data : []);

            updateKpis(items);

            const paginator = new TablePagination(items, DEFAULT_PAGINATION_LIMIT, (pagedData) => {
                inventoryTable.setData(pagedData);
            });

            paginator.init();
            inventoryTable.setData(paginator.getCurrentPageData());
        } else {
		    toast.show(response.message || 'Error al cargar inventario', 'error');
		    inventoryTable.setData([]);
		}
    } catch (error) {
        toast.show('No se pudo cargar la información de inventario. ' + (error.message || ''), 'error');
        inventoryTable.setData([]);
    }
}

// Actualiza los KPIs del inventario
function updateKpis(items) {
    const kpis = document.querySelectorAll('.card-kpi');
    if (kpis.length === 0) return;

    const totalProductos = items.length;

    let valorTotal = 0;
    let stockBajo = 0;
    let sinStock = 0;

    items.forEach(item => {
        const product = item.product || {};
        const salePrice = parseFloat(product.sale_price) || 0;
        valorTotal += item.quantity * salePrice;

        if (item.quantity === 0) {
            sinStock++;
        } else if (item.quantity < 10) {
            stockBajo++;
        }
    });

    const values = [
        totalProductos.toLocaleString(),
        `€ ${valorTotal.toLocaleString('es-ES', { minimumFractionDigits: 2 })}`,
        stockBajo.toString(),
        sinStock.toString()
    ];

    kpis.forEach((kpi, index) => {
        const valueEl = kpi.querySelector('.card-kpi-value');
        if (valueEl && values[index]) {
            valueEl.textContent = values[index];
        }
    });
}

document.addEventListener('DOMContentLoaded', initInventoryPage);
