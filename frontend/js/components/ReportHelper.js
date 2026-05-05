import { authService } from '../services/AuthService.js';
import { create, clearChildren } from '../utils/dom.js';
import { SearchableSelect } from './SearchableSelect.js';

// Utilidades para inicialización y gestión de reportes

export class ReportHelper {
    // Inicializa los componentes básicos del reporte
    static async init(config) {
        // Inicializar barra lateral
        if (window.sidebar) {
            window.sidebar.init(config.sidebarId || 'reports/index.html');
        }

        // Verificar autenticación
        if (!authService.isAuthenticated()) {
            window.location.href = '/index.html';
            return false;
        }

        // Inicializar encabezado
        if (window.pageHeader) {
            window.pageHeader.init(config.title, {
                showSearch: config.showSearch || false,
                extraActions: null
            });
        }

        // Configurar el botón de exportación PDF existente en el DOM
        const btnExport = document.getElementById('btn-export-pdf');
        if (btnExport && (config.pdfUrl || config.pdfEndpoint)) {
            this.setupPdfButton(btnExport, config.pdfEndpoint || config.pdfUrl, config.getPdfParams, config.pdfFileName || config.title);
        }

        // Inicializar selects buscables en los filtros
        setTimeout(() => {
            SearchableSelect.initAll('.card-body');
        }, 100);

        return true;
    }

    // Extrae filtros automáticamente de elementos con ID 'report-filter-*'
    static getFilters() {
        const filters = {};
        const filterElements = document.querySelectorAll('[id^="report-filter-"]');
        filterElements.forEach(el => {
            // Omitir si el elemento o algún ancestor visible está oculto
            if (!el.offsetParent && el.offsetHeight === 0) return;
            const val = el.value;
            // Omitir valores vacíos para no contaminar la query
            if (val === '' || val === null || val === undefined) return;
            const key = el.id.replace('report-filter-', '').replace(/-/g, '_');
            filters[key] = val;
        });
        return filters;
    }

    // Configura un botón de descarga PDF existente
    static setupPdfButton(btn, endpoint, getPdfParams, reportName) {
        if (!btn) return;

        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const { reportService } = await import('../services/ReportService.js');
            const params = getPdfParams ? getPdfParams() : this.getFilters();
            const filename = reportName || 'reporte';

            await reportService.exportToPDF(endpoint, params, filename);
        });
    }

    // Crea un badge de estado estándar
    static createBadge(text, type = 'neutral') {
        return create('span', `badge badge-${type}`, {}, text);
    }
}
