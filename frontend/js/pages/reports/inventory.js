// Configuración del reporte de inventario

import { serviceProvider } from '../../services/ServiceProvider.js';
import { formatCurrency, formatDate } from '../../utils/helpers.js';
import { ReportHelper } from '../../components/ReportHelper.js';
import { createReportPage } from '../../utils/report_utils.js';

const COLUMNS = {
    default: [
        { label: 'Producto', value: (item) => item.product_name || '-' },
        { label: 'Categoria', value: (item) => item.category || '-' },
        { label: 'Stock', value: (item) => item.quantity || 0 },
        { label: 'Precio Venta', value: (item) => formatCurrency(item.sale_price) },
        { label: 'Valor Stock', value: (item) => formatCurrency(item.stock_value) }
    ],
    low_stock: [
        { label: 'Producto', value: (item) => item.product_name || '-' },
        { label: 'Categoria', value: (item) => item.category || '-' },
        { label: 'Stock', value: (item) => item.quantity || 0 },
        { label: 'Umbral', value: (item) => item.threshold || 0 },
        { label: 'Precio Venta', value: (item) => formatCurrency(item.sale_price) }
    ],
    movements: [
        { label: 'Fecha', value: (item) => formatDate(item.created_at) },
        { label: 'Producto', value: (item) => item.product_name || '-' },
        {
            label: 'Tipo',
            value: (item) => {
                return item.movement_type === 'IN'
                    ? ReportHelper.createBadge('Entrada', 'success')
                    : ReportHelper.createBadge('Salida', 'info');
            }
        },
        { label: 'Cantidad', value: (item) => item.quantity || 0 },
        { label: 'Usuario', value: (item) => item.user || '-' }
    ]
};

// Procesa los datos del inventario según la vista seleccionada
function processInventoryData(data, filters, columns) {
    const view = filters.view || '';
    const columnsToUse = columns[view] || columns.default;
    const processedData = Array.isArray(data) ? data : (data ? [data] : []);
    return { data: processedData, columns: columnsToUse };
}

createReportPage({
    title: 'Reporte de Inventario',
    sidebarId: 'reports/inventory.html',
    pdfEndpoint: '/v1/reports/inventory/',
    pdfFileName: 'reporte_inventario',
    serviceMethod: (filters) => serviceProvider.reports.getReportsInventories(filters),
    columns: COLUMNS,
    groupByField: 'view',
    processData: processInventoryData,
    onInit: () => {
        const selectView = document.getElementById('report-filter-view');
        const groupThreshold = document.getElementById('group-threshold');

        if (selectView && groupThreshold) {
            selectView.addEventListener('change', () => {
                groupThreshold.style.display = selectView.value === 'low_stock' ? 'block' : 'none';
            });
        }
    }
});
