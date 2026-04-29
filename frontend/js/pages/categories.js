/**
 * CATEGORIES.JS
 * Inicializa los componentes de la página Categorías:
 *  - Sidebar con la página activa marcada
 *  - Header con título "Categorías" y botón "Nueva Categoría"
 *  - Modal de "Nueva Categoría" (abrir/cerrar desde el header)
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Inicializar componentes ───────────────────────────────────
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
