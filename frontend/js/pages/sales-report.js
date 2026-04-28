/**
 * REPORTS/SALES.JS
 * Inicializa la página Reporte de Ventas:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Reporte de Ventas"
 *  - Cambiar entre vistas según la selección del filtro "Vista / Agrupación"
 *  - Botones de Generar Reporte y Exportar PDF
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('reports/sales.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Reporte de Ventas');
    }

    // ─── Cambio de vista según el selector ─────────────────────────
    const viewSelect = document.getElementById('report-view');
    const views = {
        general:  document.getElementById('view-general'),
        customer: document.getElementById('view-customer'),
        payment:  document.getElementById('view-payment'),
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
            console.log('Generar reporte de ventas');
        });
    }

    // ─── Botón Exportar PDF ────────────────────────────────────────
    const btnExport = document.getElementById('btn-export-pdf');
    if (btnExport) {
        btnExport.addEventListener('click', function () {
            // El backend conectará aquí el GET
            console.log('Exportar reporte de ventas a PDF');
        });
    }

});
