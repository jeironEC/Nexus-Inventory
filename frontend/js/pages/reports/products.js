// Configuración del reporte de productos

import { serviceProvider } from '../../services/ServiceProvider.js';
import { formatCurrency } from '../../utils/helpers.js';
import { createReportPage } from '../../utils/report_utils.js';

const COLUMNS = {
    top_seling: [
        { label: 'Producto', value: (item) => item.product_name || '-' },
        { label: 'Categoria', value: (item) => item.category || '-' },
        { label: 'Cant. Vendida', value: (item) => item.total_quantity_sold || 0 },
        { label: 'Ingresos', value: (item) => formatCurrency(item.total_revenue) }
    ],
    most_purchased: [
        { label: 'Producto', value: (item) => item.product_name || '-' },
        { label: 'Categoria', value: (item) => item.category || '-' },
        { label: 'Cant. Comprada', value: (item) => item.total_quantity_purchased || 0 },
        { label: 'Gasto', value: (item) => formatCurrency(item.total_spent) }
    ],
    low_seling: [
        { label: 'Producto', value: (item) => item.product_name || '-' },
        { label: 'Categoria', value: (item) => item.category || '-' },
        { label: 'Cant. Vendida', value: (item) => item.total_quantity_sold || 0 },
        { label: 'Ingresos', value: (item) => formatCurrency(item.total_revenue) }
    ],
    by_category: [
        { label: 'Categoría', value: (item) => item.category_name || '-' },
        { label: 'Total Productos', value: (item) => item.total_products || 0 },
        { label: 'Cant. Vendida', value: (item) => item.total_quantity_sold || 0 },
        { label: 'Ingresos', value: (item) => formatCurrency(item.total_revenue) }
    ],
    by_supplier: [
        { label: 'Proveedor', value: (item) => item.supplier_name || '-' },
        { label: 'Total Productos', value: (item) => item.total_products || 0 },
        { label: 'Cant. Comprada', value: (item) => item.total_quantity_purchased || 0 },
        { label: 'Gasto Total', value: (item) => formatCurrency(item.total_spent) }
    ]
};

// Procesa los datos de productos según la vista seleccionada
function processProductsData(data, filters, columns) {
    const view = filters.view || 'top_seling';
    const columnsToUse = columns[view] || columns.top_seling;
    const processedData = Array.isArray(data) ? data : (data ? [data] : []);
    return { data: processedData, columns: columnsToUse };
}

createReportPage({
    title: 'Reporte de Productos',
    sidebarId: 'reports/products.html',
    pdfEndpoint: '/v1/reports/products/',
    pdfFileName: 'reporte_productos',
    serviceMethod: (filters) => serviceProvider.reports.getReportsProducts(filters),
    columns: COLUMNS,
    groupByField: 'view',
    processData: processProductsData,
    onInit: () => {
        const selectView = document.getElementById('report-filter-view');
        const groupLimit = document.getElementById('report-filter-limit');

        if (selectView && groupLimit) {
            selectView.addEventListener('change', () => {
                groupLimit.closest('.form-group').style.display = selectView.value === 'by_category' || selectView.value === 'by_supplier' ? 'none' : '';
            });
        }
    }
});
