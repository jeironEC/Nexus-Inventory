/**
 * REPORTS/INVENTORY.JS
 * Inicializa la página Reporte de Inventario:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Reporte de Inventario"
 *  - Cambiar entre vistas según la selección del filtro "Vista"
 *  - Botones de Generar Reporte y Exportar PDF
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('reports/inventory.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Reporte de Inventario');
    }

    // ─── Cambio de vista según el selector ─────────────────────────
    const viewSelect = document.getElementById('report-view');
    const views = {
        general:    document.getElementById('view-general'),
        low_stock:  document.getElementById('view-low-stock'),
        movements:  document.getElementById('view-movements')
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
            // El backend conectará aquí el GET con los filtros
            console.log('Generar reporte de inventario');
        });
    }

    // ─── Botón Exportar PDF ────────────────────────────────────────
    const btnExport = document.getElementById('btn-export-pdf');
    if (btnExport) {
        btnExport.addEventListener('click', function () {
            // El backend conectará aquí el GET de exportación PDF
            console.log('Exportar reporte de inventario a PDF');
        });
    }

});
