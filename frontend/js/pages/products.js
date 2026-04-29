/**
 * PRODUCTS.JS
 * Inicializa los componentes de la página Productos:
 *  - Sidebar con la página activa marcada
 *  - Header con título "Productos" y botón "Nuevo Producto"
 *  - Toggle entre vista normal y vista de auditoría
 *  - Modal de "Nuevo Producto"
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

    // ─── Toggle vistas ─────────────────────────────────────────────
    const btnNormal  = document.getElementById('btn-view-normal');
    const btnAudit   = document.getElementById('btn-view-audit');
    const viewNormal = document.getElementById('view-normal');
    const viewAudit  = document.getElementById('view-audit');

    if (btnNormal && btnAudit) {
        btnNormal.addEventListener('click', function () {
            viewNormal.style.display = 'block';
            viewAudit.style.display  = 'none';
            btnNormal.classList.add('active');
            btnAudit.classList.remove('active');
        });

        btnAudit.addEventListener('click', function () {
            viewAudit.style.display  = 'block';
            viewNormal.style.display = 'none';
            btnAudit.classList.add('active');
            btnNormal.classList.remove('active');
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
