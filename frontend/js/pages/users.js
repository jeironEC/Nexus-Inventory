/**
 * USERS.JS
 * Inicializa los componentes de la página Usuarios:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Usuarios"
 *  - Modal de "Nuevo Usuario" (abrir/cerrar)
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('users.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Usuarios', {
            icon: 'person_add',
            text: 'Nuevo Usuario',
            onClick: function () {
                if (window.modal) {
                    window.modal.show('modal-new-user');
                }
            }
        });
    }

    const formNewUser = document.getElementById('form-new-user');
    if (formNewUser) {
        formNewUser.addEventListener('submit', function (e) {
            e.preventDefault();
            console.log('Formulario nuevo usuario enviado');
        });
    }

});
