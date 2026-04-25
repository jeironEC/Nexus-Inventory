/**
 * INVENTORY.JS
 * Inicializa los componentes de la página Inventario:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Inventario"
 *
 * SIN fetch ni conexiones a API.
 * Las KPIs y la tabla los rellenará el compañero de backend.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('inventory.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Inventario');
    }

});
