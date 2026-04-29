/**
 * INVENTORY.JS
 * Inicializa los componentes de la página Inventario:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Inventario"
 *  - Toggle entre vista normal y vista de auditoría
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('inventory.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Inventario');
    }

    // ─── Toggle vistas ─────────────────────────────────────────────
    const btnNormal = document.getElementById('btn-view-normal');
    const btnAudit  = document.getElementById('btn-view-audit');
    const viewNormal = document.getElementById('view-normal');
    const viewAudit  = document.getElementById('view-audit');

    if (btnNormal && btnAudit) {
        btnNormal.addEventListener('click', function () {
            viewNormal.style.display = 'block';
            viewAudit.style.display  = 'none';
            btnNormal.classList.add('active');
            btnAudit.classList.remove('active');
        });

        btnAudit.addEventListener('click', function () {
            viewAudit.style.display  = 'block';
            viewNormal.style.display = 'none';
            btnAudit.classList.add('active');
            btnNormal.classList.remove('active');
        });
    }

});
