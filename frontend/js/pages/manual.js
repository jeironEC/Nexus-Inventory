/**
 * MANUAL.JS
 * Inicializa los componentes de la página Manual de Uso:
 *  - Sidebar con la página activa marcada
 *  - Header con el título
 *
 * Página estática, sin fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('manual.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Manual de Uso');
    }

});
