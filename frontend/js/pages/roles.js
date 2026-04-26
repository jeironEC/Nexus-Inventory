/**
 * ROLES.JS
 * Inicializa los componentes de la página Roles:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Roles"
 *  - Modal de "Nuevo Rol" (abrir/cerrar)
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Inicializar componentes ───────────────────────────────────
    if (window.sidebar) {
        window.sidebar.init('roles.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Roles');
    }

    // ─── Modal de crear rol ────────────────────────────────────────
    const btnNewRole = document.getElementById('btn-new-role');
    const modalNewRole = document.getElementById('modal-new-role');

    if (btnNewRole && modalNewRole) {
        btnNewRole.addEventListener('click', function () {
            if (window.modal) {
                window.modal.show('modal-new-role');
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
