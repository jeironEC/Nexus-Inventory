/**
 * CUSTOMERS.JS
 * Inicializa los componentes de la página Clientes:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Clientes"
 *  - Modal de "Nuevo Cliente" (abrir/cerrar)
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('customers.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Clientes');
    }

    // ─── Modal de crear cliente ────────────────────────────────────
    const btnNewCustomer = document.getElementById('btn-new-customer');
    const modalNewCustomer = document.getElementById('modal-new-customer');

    if (btnNewCustomer && modalNewCustomer) {
        btnNewCustomer.addEventListener('click', function () {
            if (window.modal) {
                window.modal.show('modal-new-customer');
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
