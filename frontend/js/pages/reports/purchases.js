// Configuración del reporte de compras

import { serviceProvider } from '../../services/ServiceProvider.js';
import { formatCurrency } from '../../utils/helpers.js';
import { createReportPage } from '../../utils/report_utils.js';

const COLUMNS = {
    summary: [
        { label: 'Total Compras', value: (item) => item.total_purchases || 0 },
        { label: 'Gasto Total', value: (item) => formatCurrency(item.total_spent) },
        { label: 'Impuestos', value: (item) => formatCurrency(item.total_tax) },
        { label: 'Ticket Promedio', value: (item) => formatCurrency(item.average_ticket) },
        { label: 'Canceladas', value: (item) => item.canceled_purchases || 0 }
    ],
    supplier: [
        { label: 'Proveedor', value: (item) => item.supplier_name || '-' },
        { label: 'Total Compras', value: (item) => item.total_purchases || 0 },
        { label: 'Gasto Total', value: (item) => formatCurrency(item.total_spent) }
    ],
    period: [
        { label: 'Periodo', value: (item) => {
            const p = item.period || '-';
            if (typeof p === 'string' && p.length === 7 && p.includes('-')) {
                const [year, month] = p.split('-');
                return `${month}/${year}`;
            }
            return p;
        }},
        { label: 'Total Compras', value: (item) => item.total_purchases || 0 },
        { label: 'Gasto Total', value: (item) => formatCurrency(item.total_spent) }
    ]
};

// Procesa los datos de compras según el agrupamiento seleccionado
function processPurchasesData(data, filters, columns) {
    const groupBy = filters.group_by || '';
    let processedColumns = columns[groupBy] || columns.summary;
    let processedData = [];

    if (!groupBy) {
        if (data && !Array.isArray(data)) {
            processedData = [data];
        } else if (Array.isArray(data) && data.length > 0) {
            processedData = data;
        }
    } else {
        processedData = Array.isArray(data) ? data : [];
    }

    return { data: processedData, columns: processedColumns };
}

createReportPage({
    title: 'Reporte de Compras',
    sidebarId: 'reports/purchases.html',
    pdfEndpoint: '/v1/reports/purchases/',
    pdfFileName: 'reporte_compras',
    serviceMethod: (filters) => serviceProvider.reports.getReportsPurchases(filters),
    columns: COLUMNS,
    groupByField: 'group_by',
    processData: processPurchasesData,
    onInit: () => {
        const selectGroupBy = document.getElementById('report-filter-group-by');
        const groupPeriod = document.getElementById('group-period-type');

        if (selectGroupBy && groupPeriod) {
            selectGroupBy.addEventListener('change', () => {
                groupPeriod.style.display = selectGroupBy.value === 'period' ? 'block' : 'none';
            });
        }
    }
});
