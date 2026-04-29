/**
 * PRODUCTS.JS
 * Inicializa los componentes de la página Productos:
 *  - Sidebar con la página activa marcada
 *  - Header con título "Productos" y botón "Nuevo Producto"
 *  - Modal de "Nuevo Producto" (abrir/cerrar desde el header)
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('products.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Productos', {
            icon: 'add',
            text: 'Nuevo Producto',
            onClick: function () {
                if (window.modal) {
                    window.modal.show('modal-new-product');
                }
            }
        });
    }

    // ─── Submit del formulario ─────────────────────────────────────
    const formNewProduct = document.getElementById('form-new-product');
    if (formNewProduct) {
        formNewProduct.addEventListener('submit', function (e) {
            e.preventDefault();
            // El backend conectará aquí el POST
            console.log('Formulario nuevo producto enviado');
        });
    }

});
