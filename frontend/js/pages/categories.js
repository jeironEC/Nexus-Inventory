/**
 * CATEGORIES.JS
 * Inicializa los componentes de la página Categorías:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Categorías"
 *  - Modal de "Nueva Categoría" (abrir/cerrar)
 *
 * SIN fetch ni conexiones a API.
 * El compañero conectará el GET (tabla, filtros) y el POST (crear categoría).
 */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Inicializar componentes ───────────────────────────────────
    if (window.sidebar) {
        window.sidebar.init('categories.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Categorías');
    }

    // ─── Modal de crear categoría ──────────────────────────────────
    const btnNewCategory = document.getElementById('btn-new-category');
    const modalNewCategory = document.getElementById('modal-new-category');

    if (btnNewCategory && modalNewCategory) {
        btnNewCategory.addEventListener('click', function () {
            if (window.modal) {
                window.modal.show('modal-new-category');
            }
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
