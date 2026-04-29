/**
 * PURCHASE_RETURNS.JS
 * Inicializa los componentes de la página Devoluciones de Compra:
 *  - Sidebar con la página activa marcada
 *  - Header con título "Devoluciones de Compra" y botón "Nueva Devolución"
 *  - Modal de "Nueva Devolución" (abrir/cerrar desde el header)
 *  - Añadir/eliminar filas de productos en el modal
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('purchase_returns.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Devoluciones de Compra', {
            icon: 'keyboard_return',
            text: 'Nueva Devolución',
            onClick: function () {
                if (window.modal) {
                    window.modal.show('modal-new-purchase-return');
                }
            }
        });
    }

    // ─── Añadir / eliminar filas de productos ──────────────────────
    const btnAddProduct = document.getElementById('btn-add-product');
    const detailsTbody  = document.getElementById('purchase-return-details-tbody');

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

    // ─── Crear una nueva fila de producto ──────────────────────────
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

        // Coste unitario
        const tdCost = document.createElement('td');
        const inputCost = document.createElement('input');
        inputCost.type = 'number';
        inputCost.step = '0.01';
        inputCost.className = 'form-input';
        inputCost.name = 'unit_cost';
        inputCost.placeholder = '0.00';
        tdCost.appendChild(inputCost);

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
        tr.appendChild(tdCost);
        tr.appendChild(tdSubtotal);
        tr.appendChild(tdActions);

        return tr;
    }

    // ─── Submit del formulario ─────────────────────────────────────
    const formNewReturn = document.getElementById('form-new-purchase-return');
    if (formNewReturn) {
        formNewReturn.addEventListener('submit', function (e) {
            e.preventDefault();
            // El backend conectará aquí el POST
            console.log('Formulario nueva devolución de compra enviado');
        });
    }

});
