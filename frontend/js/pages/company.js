/**
 * COMPANY.JS
 * Inicializa la página de Perfil Empresa:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Perfil Empresa"
 *  - Cambiar logo (preview local)
 *  - Submit del formulario
 *  - Confirmación al eliminar empresa
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('company.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Perfil Empresa');
    }

    // ─── Submit: información de la empresa ─────────────────────────
    const form = document.getElementById('form-company-info');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            // El cbackend conectará aquí el PATCH
            console.log('Formulario empresa enviado');
        });
    }
});
