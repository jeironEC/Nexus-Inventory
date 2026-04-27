/**
 * INVOICES.JS
 * Inicializa los componentes de la página Facturas:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Facturas"
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('invoices.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Facturas');
    }

});
