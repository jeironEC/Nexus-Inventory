/**
 * TERMS.JS
 * Inicializa los componentes de la página Términos y Condiciones:
 *  - Sidebar con la página activa marcada
 *  - Header con el título
 *
 * Página estática, sin fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('terms.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Términos y Condiciones');
    }

});
