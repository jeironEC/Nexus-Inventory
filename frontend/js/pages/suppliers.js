/**
 * SUPPLIERS.JS
 * Inicializa los componentes de la página Proveedores:
 *  - Sidebar con la página activa marcada
 *  - Header con título "Proveedores" y botón "Nuevo Proveedor"
 *  - Toggle entre vista normal y vista de auditoría
 *  - Modal de "Nuevo Proveedor"
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
    const formNewSupplier = document.getElementById('form-new-supplier');
    if (formNewSupplier) {
        formNewSupplier.addEventListener('submit', function (e) {
            e.preventDefault();
            // El backend conectará aquí el POST
            console.log('Formulario nuevo proveedor enviado');
        });
    }

});
