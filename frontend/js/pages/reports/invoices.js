// Lógica del reporte de facturación

import { serviceProvider } from '../../services/ServiceProvider.js';
import { formatCurrency, formatDate } from '../../utils/helpers.js';
import { ReportHelper } from '../../components/ReportHelper.js';
import { ReportTable } from '../../components/ReportTable.js';

let reportTable;

const COLUMNS = [
    { label: 'Nº Factura', value: (item) => item.number_invoice || `#${item.id}` },
    { label: 'Fecha Emisión', value: (item) => formatDate(item.created_at) },
    {
        label: 'Cliente / Proveedor',
        value: (item) => {
            const name = item.sale__customer__first_name
                ? `${item.sale__customer__first_name} ${item.sale__customer__last_name || ''}`.trim()
                : (item.purchase__supplier__name || 'N/A');
            return name;
        }
    },
    {
        label: 'Monto Total',
        value: (item) => formatCurrency(item.sale__total_amount || item.purchase__total_amount || 0)
    },
    {
        label: 'Estado',
        value: (item) => {
            return item.state === 'ISSUED'
                ? ReportHelper.createBadge('Emitida', 'success')
                : ReportHelper.createBadge('Cancelada', 'danger');
        }
    }
];

// Inicializa el reporte de facturación
async function initReport() {
    await ReportHelper.init({
        title: 'Reporte de Facturación',
        sidebarId: 'reports/invoices.html',
        pdfEndpoint: '/v1/reports/invoices/',
        pdfFileName: 'reporte_facturas'
    });

    document.getElementById('btn-apply-filters')?.addEventListener('click', loadReportData);
    await loadReportData();
}

// Carga los datos del reporte desde el servicio
async function loadReportData() {
    const filters = ReportHelper.getFilters();

    reportTable.showLoading();

    try {
        const response = await serviceProvider.reports.getReportsInvoices(filters);

        if (response.success && response.data) {
            const data = Array.isArray(response.data.data) ? response.data.data : [];
            reportTable.setData(data, COLUMNS);
        } else {
            reportTable.showError(response.message || 'Error al cargar datos');
        }
    } catch (error) {
        reportTable.showError('Error de conexión con el servidor');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    reportTable = new ReportTable({
        selector: '#report-table',
        defaultColumns: COLUMNS,
        emptyMessage: 'No hay registros disponibles'
    });

    initReport();
});
