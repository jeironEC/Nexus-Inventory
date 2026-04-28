/**
 * REPORTS/PURCHASES.JS
 * Inicializa la página Reporte de Compras:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Reporte de Compras"
 *  - Cambiar entre vistas según la selección del filtro "Vista / Agrupación"
 *  - Botones de Generar Reporte y Exportar PDF
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('reports/purchases.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Reporte de Compras');
    }

    // ─── Cambio de vista según el selector ─────────────────────────
    const viewSelect = document.getElementById('report-view');
    const views = {
        general:  document.getElementById('view-general'),
        supplier: document.getElementById('view-supplier'),
        period:   document.getElementById('view-period')
    };

    function showView(key) {
        Object.keys(views).forEach(function (k) {
            if (!views[k]) return;
            if (k === key) {
                views[k].classList.remove('hidden');
            } else {
                views[k].classList.add('hidden');
            }
        });
    }

    if (viewSelect) {
        viewSelect.addEventListener('change', function () {
            showView(viewSelect.value);
        });
    }

    // ─── Botón Generar Reporte ─────────────────────────────────────
    const btnGenerate = document.getElementById('btn-generate-report');
    if (btnGenerate) {
        btnGenerate.addEventListener('click', function () {
            // El backend conectará aquí el GET
            console.log('Generar reporte de compras');
        });
    }

    // ─── Botón Exportar PDF ────────────────────────────────────────
    const btnExport = document.getElementById('btn-export-pdf');
    if (btnExport) {
        btnExport.addEventListener('click', function () {
            // El backend conectará aquí el GET
            console.log('Exportar reporte de compras a PDF');
        });
    }

});
