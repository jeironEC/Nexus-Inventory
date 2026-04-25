/**
 * DASHBOARD.JS
 * Inicializa los componentes del dashboard:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Dashboard"
 *
 * SIN fetch ni conexiones a API.
 * Las tablas y KPIs los rellenará el backend.
 */

document.addEventListener('DOMContentLoaded', function () {

    // Inicializar sidebar
    if (window.sidebar) {
        window.sidebar.init('index.html');
    }

    // Inicializar header
    if (window.pageHeader) {
        window.pageHeader.init('Dashboard');
    }

});
