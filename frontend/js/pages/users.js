/**
 * USERS.JS
 * Inicializa los componentes de la página Usuarios:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Usuarios"
 *  - Modal de "Nuevo Usuario" (abrir/cerrar)
 *
 * SIN fetch ni conexiones a API.
 * El compañero conectará el GET (tabla, filtros) y el POST (crear usuario).
 */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Inicializar componentes ───────────────────────────────────
    if (window.sidebar) {
        window.sidebar.init('users.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Usuarios');
    }

    // ─── Modal de crear usuario ────────────────────────────────────
    const btnNewUser = document.getElementById('btn-new-user');
    const modalNewUser = document.getElementById('modal-new-user');

    if (btnNewUser && modalNewUser) {
        // Abrir modal
        btnNewUser.addEventListener('click', function () {
            if (window.modal) {
                window.modal.show('modal-new-user');
            }
        });
    }

    // ─── Submit del formulario ─────────────────────────────────────
    const formNewUser = document.getElementById('form-new-user');
    if (formNewUser) {
        formNewUser.addEventListener('submit', function (e) {
            e.preventDefault();
            // El backend conectará aquí el POST
            console.log('Formulario nuevo usuario enviado');
        });
    }

});
