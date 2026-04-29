/**
 * ROLES.JS
 * Inicializa los componentes de la página Roles:
 *  - Sidebar con la página activa marcada
 *  - Header con título "Roles" y botón "Nuevo Rol"
 *  - Modal de "Nuevo Rol" (abrir/cerrar desde el header)
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Inicializar componentes ───────────────────────────────────
    if (window.sidebar) {
        window.sidebar.init('roles.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Roles', {
            icon: 'admin_panel_settings',
            text: 'Nuevo Rol',
            onClick: function () {
                if (window.modal) {
                    window.modal.show('modal-new-role');
                }
            }
        });
    }

    // ─── Submit del formulario ─────────────────────────────────────
    const formNewRole = document.getElementById('form-new-role');
    if (formNewRole) {
        formNewRole.addEventListener('submit', function (e) {
            e.preventDefault();
            // El backend conectará aquí el POST
            console.log('Formulario nuevo rol enviado');
        });
    }

});
