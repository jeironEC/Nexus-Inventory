/**
 * SALE_RETURNS.JS
 * Inicializa los componentes de la página Devoluciones de Venta:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Devoluciones de Venta"
 *  - Modal de "Nueva Devolución" (abrir/cerrar)
 *  - Añadir/eliminar filas de productos en el modal
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('sale_returns.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Devoluciones de Venta');
    }

    // ─── Modal de crear devolución ─────────────────────────────────
    const btnNewReturn = document.getElementById('btn-new-sale-return');
    const modalNewReturn = document.getElementById('modal-new-sale-return');

    if (btnNewReturn && modalNewReturn) {
        btnNewReturn.addEventListener('click', function () {
            if (window.modal) {
                window.modal.show('modal-new-sale-return');
            }
        });
    }

    // ─── Añadir / eliminar filas de productos ──────────────────────
    const btnAddProduct = document.getElementById('btn-add-product');
    const detailsTbody  = document.getElementById('sale-return-details-tbody');

    if (btnAddProduct && detailsTbody) {
        btnAddProduct.addEventListener('click', function () {
            const newRow = createProductRow();
            detailsTbody.appendChild(newRow);
        });

        detailsTbody.addEventListener('click', function (e) {
            const removeBtn = e.target.closest('.btn-remove-row');
            if (removeBtn) {
                const row = removeBtn.closest('tr');
                if (row && detailsTbody.querySelectorAll('.return-detail-row').length > 1) {
                    row.remove();
                }
            }
        });
    }

    // ─── Crear una nueva fila de producto ──────────
    function createProductRow() {
        const tr = document.createElement('tr');
        tr.className = 'return-detail-row';

        // Producto
        const tdProduct = document.createElement('td');
        const selectProduct = document.createElement('select');
        selectProduct.className = 'form-input';
        selectProduct.name = 'product_id';
        const optionDefault = document.createElement('option');
        optionDefault.value = '';
        optionDefault.textContent = 'Selecciona producto';
        selectProduct.appendChild(optionDefault);
        tdProduct.appendChild(selectProduct);

        // Cantidad
        const tdQty = document.createElement('td');
        const inputQty = document.createElement('input');
        inputQty.type = 'number';
        inputQty.className = 'form-input';
        inputQty.name = 'quantity';
        inputQty.placeholder = '1';
        inputQty.min = '1';
        inputQty.value = '1';
        tdQty.appendChild(inputQty);

        // Precio unitario
        const tdPrice = document.createElement('td');
        const inputPrice = document.createElement('input');
        inputPrice.type = 'number';
        inputPrice.step = '0.01';
        inputPrice.className = 'form-input';
        inputPrice.name = 'unit_price';
        inputPrice.placeholder = '0.00';
        tdPrice.appendChild(inputPrice);

        // Subtotal
        const tdSubtotal = document.createElement('td');
        tdSubtotal.className = 'return-detail-subtotal';
        tdSubtotal.textContent = '€ 0.00';

        // Botón eliminar
        const tdActions = document.createElement('td');
        const btnRemove = document.createElement('button');
        btnRemove.type = 'button';
        btnRemove.className = 'table-action-btn danger btn-remove-row';
        btnRemove.title = 'Eliminar';
        const iconRemove = document.createElement('span');
        iconRemove.className = 'material-symbols-outlined';
        iconRemove.textContent = 'delete';
        btnRemove.appendChild(iconRemove);
        tdActions.appendChild(btnRemove);

        tr.appendChild(tdProduct);
        tr.appendChild(tdQty);
        tr.appendChild(tdPrice);
        tr.appendChild(tdSubtotal);
        tr.appendChild(tdActions);

        return tr;
    }

    // ─── Submit del formulario ─────────────────────────────────────
    const formNewReturn = document.getElementById('form-new-sale-return');
    if (formNewReturn) {
        formNewReturn.addEventListener('submit', function (e) {
            e.preventDefault();
            // El backend conectará aquí el POST
            console.log('Formulario nueva devolución enviado');
        });
    }

});
