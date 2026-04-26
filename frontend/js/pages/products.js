/**
 * PRODUCTS.JS
 * Inicializa los componentes de la página Productos:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Productos"
 *  - Modal de "Nuevo Producto" (abrir/cerrar)
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('products.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Productos');
    }

    // ─── Modal de crear producto ───────────────────────────────────
    const btnNewProduct = document.getElementById('btn-new-product');
    const modalNewProduct = document.getElementById('modal-new-product');

    if (btnNewProduct && modalNewProduct) {
        btnNewProduct.addEventListener('click', function () {
            if (window.modal) {
                window.modal.show('modal-new-product');
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
