// Servicio para gestionar reportes y exportaciones

import { authService } from "./AuthService.js";
import {
    URL_REPORTS_CUSTOMERS,
    URL_REPORTS_INVENTORIES,
    URL_REPORTS_INVOICES,
    URL_REPORTS_PRODUCTS,
    URL_REPORTS_PURCHASES,
    URL_REPORTS_RETURNS,
    URL_REPORTS_SALES
} from "../utils/const.js";

class ReportService {
    get api() {
        return authService.getApiClient();
    }

    // Exporta un reporte a PDF
    async exportToPDF(endpoint, filters, filenamePrefix) {
        try {
            if (window.modal) {
                window.modal.showLoading('Información', 'Generando y descargando PDF...');
            }

            const params = new URLSearchParams(filters).toString();
            let url = endpoint;
            if (!url.endsWith('/')) url += '/';
            url += 'pdf/';
            if (params) {
                url += '?' + params;
            }
            const response = await this.api.get(url, { responseType: 'blob' });

            if (response.success && response.data) {
                const filename = `${filenamePrefix}_${new Date().getTime()}.pdf`;
                const blob = response.data;
                const link = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = link;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(link);
                document.body.removeChild(a);

                if (window.modal) {
                    window.modal.showAlert('Éxito', 'PDF descargado correctamente', 'success');
                }
            } else {
                if (window.modal) {
                    window.modal.showAlert('Error', response.message || 'No se pudo generar el PDF', 'error');
                } else {
                    alert('Error: ' + (response.message || 'No se pudo generar el PDF'));
                }
            }
        } catch (error) {
            if (window.modal) {
                window.modal.showAlert('Error', 'Error de conexión al generar el PDF', 'error');
            } else {
                alert('Error de conexión al generar el PDF');
            }
        }
    }

    // Obtiene datos de reporte desde un endpoint con filtros
    async getReportData(endpoint, filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        let url = endpoint;
        if (params) {
            url += (url.includes('?') ? '&' : '?') + params;
        }
        const response = await this.api.get(url);

        // Compatibilidad con la nueva estructura { summary, data }
        if (response.success && response.data && response.data.data && Array.isArray(response.data.data)) {
            // Inyectamos results para que los controladores actuales sigan funcionando sin cambios
            response.data.results = response.data.data;
        }

        return response;
    }

    // Obtiene reporte de clientes
    getReportsCustomers(filtros) {
        return this.getReportData(URL_REPORTS_CUSTOMERS, filtros);
    }

    // Obtiene reporte de inventarios
    getReportsInventories(filtros) {
        return this.getReportData(URL_REPORTS_INVENTORIES, filtros);
    }

    // Obtiene reporte de inventarios con bajo stock
    getReportsInventoryLowStock() {
        return this.getReportsInventories({ view: 'low_stock' });
    }

    // Obtiene reporte de facturas
    getReportsInvoices(filtros) {
        return this.getReportData(URL_REPORTS_INVOICES, filtros);
    }

    // Obtiene reporte de productos
    getReportsProducts(filtros) {
        return this.getReportData(URL_REPORTS_PRODUCTS, filtros);
    }

    // Obtiene reporte de compras
    getReportsPurchases(filtros) {
        return this.getReportData(URL_REPORTS_PURCHASES, filtros);
    }

    // Obtiene reporte de devoluciones
    getReportsReturns(filtros) {
        return this.getReportData(URL_REPORTS_RETURNS, filtros);
    }

    // Obtiene reporte de ventas
    getReportsSales(filtros) {
        return this.getReportData(URL_REPORTS_SALES, filtros);
    }
}

export const reportService = new ReportService();
