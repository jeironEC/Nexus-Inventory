/**
 * SUPPLIERS.JS
 * Inicializa los componentes de la página Proveedores:
 *  - Sidebar con la página activa marcada
 *  - Header con título "Proveedores" y botón "Nuevo Proveedor"
 *  - Modal de "Nuevo Proveedor" (abrir/cerrar desde el header)
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('suppliers.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Proveedores', {
            icon: 'add_business',
            text: 'Nuevo Proveedor',
            onClick: function () {
                if (window.modal) {
                    window.modal.show('modal-new-supplier');
                }
            }
        });
    }

    // ─── Submit del formulario ─────────────────────────────────────
    const formNewSupplier = document.getElementById('form-new-supplier');
    if (formNewSupplier) {
        formNewSupplier.addEventListener('submit', function (e) {
            e.preventDefault();
            // El backend conectará aquí el POST a /v1/suppliers/
            console.log('Formulario nuevo proveedor enviado');
        });
    }

});
