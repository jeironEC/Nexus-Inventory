// Configuración del reporte de clientes

import { serviceProvider } from '../../services/ServiceProvider.js';
import { formatCurrency } from '../../utils/helpers.js';
import { createReportPage } from '../../utils/report_utils.js';

const COLUMNS = [
    { label: 'Cliente', value: (item) => item.customer_name || '-' },
    { label: 'Total Compras', value: (item) => item.total_purchases || 0 },
    { label: 'Gasto Total', value: (item) => formatCurrency(item.total_spent) }
];

createReportPage({
    title: 'Reporte de Clientes',
    sidebarId: 'reports/customers.html',
    pdfEndpoint: '/v1/reports/customers/',
    pdfFileName: 'reporte_clientes',
    serviceMethod: (filters) => serviceProvider.reports.getReportsCustomers(filters),
    columns: COLUMNS
});
