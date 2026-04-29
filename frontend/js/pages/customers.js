/**
 * CUSTOMERS.JS
 * Inicializa los componentes de la página Clientes:
 *  - Sidebar con la página activa marcada
 *  - Header con título "Clientes" y botón "Nuevo Cliente"
 *  - Modal de "Nuevo Cliente" (abrir/cerrar desde el header)
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('customers.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Clientes', {
            icon: 'person_add',
            text: 'Nuevo Cliente',
            onClick: function () {
                if (window.modal) {
                    window.modal.show('modal-new-customer');
                }
            }
        });
    }

    // ─── Submit del formulario ─────────────────────────────────────
    const formNewCustomer = document.getElementById('form-new-customer');
    if (formNewCustomer) {
        formNewCustomer.addEventListener('submit', function (e) {
            e.preventDefault();
            // El backend conectará aquí el POST
            console.log('Formulario nuevo cliente enviado');
        });
    }

});
