/**
 * REPORTS/INVOICES.JS
 * Inicializa la página Reporte de Facturación:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Reporte de Facturación"
 *  - Botones de Generar Reporte y Exportar PDF
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('reports/invoices.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Reporte de Facturación');
    }

    // ─── Botón Generar Reporte ─────────────────────────────────────
    const btnGenerate = document.getElementById('btn-generate-report');
    if (btnGenerate) {
        btnGenerate.addEventListener('click', function () {
            // El backend conectará aquí el GET con los filtros
            console.log('Generar reporte de facturación');
        });
    }

    // ─── Botón Exportar PDF ────────────────────────────────────────
    const btnExport = document.getElementById('btn-export-pdf');
    if (btnExport) {
        btnExport.addEventListener('click', function () {
            // El backend conectará aquí el GET de exportación PDF
            console.log('Exportar reporte de facturación a PDF');
        });
    }

});
