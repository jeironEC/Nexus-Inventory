// Configuración del reporte de ventas

import { serviceProvider } from '../../services/ServiceProvider.js';
import { formatCurrency } from '../../utils/helpers.js';
import { createReportPage } from '../../utils/report_utils.js';

const COLUMNS = {
    summary: [
        { label: 'Total Ventas', value: (item) => item.total_sales || 0 },
        { label: 'Ingresos Totales', value: (item) => formatCurrency(item.total_revenue) },
        { label: 'Impuestos', value: (item) => formatCurrency(item.total_tax) },
        { label: 'Ticket Promedio', value: (item) => formatCurrency(item.average_ticket) },
        { label: 'Canceladas', value: (item) => item.canceled_sales || 0 }
    ],
    customer: [
        { label: 'Cliente', value: (item) => item.customer_name || '-' },
        { label: 'Total Ventas', value: (item) => item.total_sales || 0 },
        { label: 'Ingresos', value: (item) => formatCurrency(item.total_revenue) }
    ],
    payment_method: [
        { label: 'Metodo de Pago', value: (item) => ({ CASH: 'Efectivo', CARD: 'Tarjeta', TRANSFER: 'Transferencia' }[item.payment_method] || item.payment_method_display || '-') },
        { label: 'Total Ventas', value: (item) => item.total_sales || 0 },
        { label: 'Ingresos', value: (item) => formatCurrency(item.total_revenue) }
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
        { label: 'Total Ventas', value: (item) => item.total_sales || 0 },
        { label: 'Ingresos', value: (item) => formatCurrency(item.total_revenue) }
    ]
};

// Procesa los datos de ventas según el agrupamiento seleccionado
function processSalesData(data, filters, columns) {
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
    title: 'Reporte de Ventas',
    sidebarId: 'reports/sales.html',
    pdfEndpoint: '/v1/reports/sales/',
    pdfFileName: 'reporte_ventas',
    serviceMethod: (filters) => serviceProvider.reports.getReportsSales(filters),
    columns: COLUMNS,
    groupByField: 'group_by',
    processData: processSalesData,
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
