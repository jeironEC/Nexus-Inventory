/**
 * REPORTS/CUSTOMERS.JS
 * Inicializa la página Reporte de Clientes:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Reporte de Clientes"
 *  - Cambiar entre vistas según la selección del filtro "Vista"
 *  - Botones de Generar Reporte y Exportar PDF
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('reports/customers.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Reporte de Clientes');
    }

    // ─── Cambio de vista según el selector ─────────────────────────
    const viewSelect = document.getElementById('report-view');
    const views = {
        all: document.getElementById('view-all'),
        top: document.getElementById('view-top')
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
            // El Backend conectará aquí el GET
            console.log('Generar reporte de clientes');
        });
    }

    // ─── Botón Exportar PDF ────────────────────────────────────────
    const btnExport = document.getElementById('btn-export-pdf');
    if (btnExport) {
        btnExport.addEventListener('click', function () {
            // El Backend conectará aquí el GET
            console.log('Exportar reporte de clientes a PDF');
        });
    }

});
