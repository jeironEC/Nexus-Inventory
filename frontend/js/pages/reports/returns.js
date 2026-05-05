// Configuración del reporte de devoluciones

import { serviceProvider } from '../../services/ServiceProvider.js';
import { formatCurrency, formatDate } from '../../utils/helpers.js';
import { ReportHelper } from '../../components/ReportHelper.js';
import { createReportPage } from '../../utils/report_utils.js';

const COLUMNS = [
    { label: 'Fecha', value: (item) => formatDate(item.created_at) },
    {
        label: 'Proveedor / Cliente',
        value: (item) => item.customer_name || item.supplier_name || '-'
    },
    { label: 'Motivo', value: (item) => item.reason || '-' },
    { label: 'Monto Reembolso', value: (item) => formatCurrency(item.total_amount) },
    {
        label: 'Estado',
        value: (item) => {
            return item.state === 'COMPLETED'
                ? ReportHelper.createBadge('Completada', 'success')
                : ReportHelper.createBadge('Pendiente', 'warning');
        }
    }
];

createReportPage({
    title: 'Reporte de Devoluciones',
    sidebarId: 'reports/returns.html',
    pdfEndpoint: '/v1/reports/returns/',
    pdfFileName: 'reporte_devoluciones',
    serviceMethod: (filters) => serviceProvider.reports.getReportsReturns(filters),
    columns: COLUMNS
});
