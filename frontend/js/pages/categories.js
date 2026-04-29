/**
 * CATEGORIES.JS
 * Inicializa los componentes de la página Categorías:
 *  - Sidebar con la página activa marcada
 *  - Header con título "Categorías" y botón "Nueva Categoría"
 *  - Toggle entre vista normal y vista de auditoría
 *  - Modal de "Nueva Categoría"
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('categories.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Categorías', {
            icon: 'add',
            text: 'Nueva Categoría',
            onClick: function () {
                if (window.modal) {
                    window.modal.show('modal-new-category');
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
    const formNewCategory = document.getElementById('form-new-category');
    if (formNewCategory) {
        formNewCategory.addEventListener('submit', function (e) {
            e.preventDefault();
            // El compañero conectará aquí el POST a /v1/categories/
            console.log('Formulario nueva categoría enviado');
        });
    }

});
