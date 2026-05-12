// Lógica para la gestión de compras

import { toast } from '../components/Toast.js';
import { serviceProvider } from '../services/ServiceProvider.js';
import { create, parseHTML } from '../utils/dom.js';
import { initFilterListeners, loadFilterSelects } from '../utils/filter_utils.js';
import { loadData, showModal, setupTableColumnToggles } from '../utils/base_page.js';
import { formatCurrency, formatDate, formatFullName } from '../utils/helpers.js';
import { setupDynamicDetails, getRowsData, populateSelect } from '../utils/form_utils.js';
import { TemplateLoader } from '../utils/TemplateLoader.js';
import { Table } from '../components/Table.js';

let purchaseTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `#${item.id}` },
    { label: 'Proveedor', type: 'primary', value: (item) => item.supplier?.name || 'Proveedor Desconocido' },
    { label: 'Total', type: 'normal', value: (item) => formatCurrency(item.total_amount) },
    { label: 'Estado', type: 'normal', value: (item) => `<span class="badge ${item.state === 'COMPLETED' ? 'badge-success' : 'badge-danger'}">${item.state === 'COMPLETED' ? 'Completada' : 'Cancelada'}</span>` },
    { label: 'Creado en', type: 'normal', value: (item) => item.created_at ? formatDate(item.created_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Actualizado en', type: 'normal', value: (item) => item.updated_at ? formatDate(item.updated_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Eliminado en', type: 'normal', value: (item) => item.deleted_at ? formatDate(item.deleted_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Creado por', type: 'audit', value: (item) => item.user?.first_name ? formatFullName(item.user) : (item.user?.email || '-') },
    { label: 'Actualizado por', type: 'audit', value: (item) => item.updated_by?.first_name ? formatFullName(item.updated_by) : (item.updated_by?.email || '-') },
    { label: 'Eliminado por', type: 'audit', value: (item) => item.deleted_by?.first_name ? formatFullName(item.deleted_by) : (item.deleted_by?.email || '-') }
];

// Muestra el modal con el detalle de una compra
async function handleShowPurchaseDetail(purchase) {
    const existingModal = document.getElementById('modal-purchase-detail');
    if (existingModal) existingModal.remove();

    const templateHtml = await TemplateLoader.load('purchase_detail');
    const container = create('div');
    container.appendChild(parseHTML(templateHtml));
    document.body.appendChild(container.firstElementChild);

    document.getElementById('purchase-detail-id').textContent = `#${purchase.id}`;
    document.getElementById('purchase-detail-supplier').textContent = purchase.supplier?.name || 'Proveedor desconocido';
    document.getElementById('purchase-detail-date').textContent = formatDate(purchase.created_at, 'dd/mm/yyyy HH:mm');
    document.getElementById('purchase-detail-total').textContent = formatCurrency(purchase.total_amount);

    const stateEl = document.getElementById('purchase-detail-state');
    stateEl.className = purchase.state === 'COMPLETED' ? 'badge badge-success' : 'badge badge-danger';
    stateEl.textContent = purchase.state === 'COMPLETED' ? 'Completada' : 'Cancelada';

    const tbody = document.getElementById('purchase-detail-tbody');
    tbody.innerHTML = '<tr><td colspan="4" class="text-center"><div class="spinner spinner-sm"></div></td></tr>';

    window.modal.show('modal-purchase-detail');

    try {
        const response = await serviceProvider.purchases.getDetailsPurchaseById(purchase.id);
        if (response.success && response.data) {
            const items = response.data.results || response.data;
            tbody.innerHTML = items.map(item => `
                <tr>
                    <td>${item.product?.name || 'Producto desconocido'}</td>
                    <td>${item.quantity}</td>
                    <td>${formatCurrency(item.unit_cost)}</td>
                    <td>${formatCurrency(item.subtotal)}</td>
                </tr>
            `).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">Error al cargar detalles</td></tr>';
        }
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center">Error de conexión</td></tr>';
    }
}

// Inicializa la página de compras
async function initPurchasesPage() {
    if (window.sidebar) {
        window.sidebar.init('purchases.html');
    }

    setupPurchasesPageHeader();

    purchaseTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
        actions: {
            customHtml: (item) => `
                <div class="table-actions">
                    <button class="btn-action btn-view-detail" title="Ver Detalle">
                        <span class="material-symbols-outlined">visibility</span>
                    </button>
                    ${item.state === 'COMPLETED' ? `
                    <button class="btn-action btn-action-danger btn-cancel-purchase" title="Cancelar Compra">
                        <span class="material-symbols-outlined">cancel</span>
                    </button>` : '<span style="color: rgba(206,232,242,0.3); font-size: 12px;">—</span>'}
                </div>
            `,
            setupEvents: (tr, item) => {
                const btnView = tr.querySelector('.btn-view-detail');
                if (btnView) btnView.addEventListener('click', () => handleShowPurchaseDetail(item));
                const btnCancel = tr.querySelector('.btn-cancel-purchase');
                if (btnCancel) btnCancel.addEventListener('click', () => handleCancelPurchase(item));
            }
        }
    });

    setupTableColumnToggles();

    // Cargar opciones de proveedores en el select de filtros
    await loadFilterSelects(['purchase-filter-supplier-id']);

    await loadPurchasesData();

    initFilterListeners('.card', async () => {
        await loadPurchasesData();
    });
}

// Carga los datos de las compras
async function loadPurchasesData() {
    await loadData({
        service: serviceProvider.purchases,
        renderFn: (data) => purchaseTable.setData(data)
    });
}

// Cancela una compra
async function handleCancelPurchase(purchase) {
    window.modal.showConfirm(
        'Cancelar Compra',
        `¿Estás seguro de que deseas cancelar la compra #${purchase.id}? Esta acción revertirá el inventario agregado.`,
        async () => {
            try {
                const response = await serviceProvider.purchases.cancel(purchase.id);
                if (response.success) {
                    await loadPurchasesData();
                    toast.show('Compra cancelada exitosamente', 'success');
                } else {
                    window.modal.showAlert('Error', response.message || 'No se pudo cancelar la compra', 'error');
                }
            } catch (error) {
                window.modal.showAlert('Error', error.message || 'Error al cancelar la compra', 'error');
            }
        }
    );
}

// Configura el encabezado de la página
function setupPurchasesPageHeader() {
    const btnNew = create('button', 'btn btn-primary', { id: 'btn-new-purchase' });
    btnNew.appendChild(create('span', 'material-symbols-outlined', {}, 'add'));
    btnNew.appendChild(document.createTextNode('Nueva Compra'));

    btnNew.addEventListener('click', () => handleShowPurchaseModal());

    if (window.pageHeader) {
        window.pageHeader.init('Compras', { extraActions: btnNew });
    }
}

// Muestra el modal para crear una nueva compra
async function handleShowPurchaseModal() {
    await showModal({
        modalId: 'modal-purchase',
        template: 'purchase',
        formId: 'form-purchase',
        singularName: 'Compra',
        onSubmit: handlePurchaseSubmit,
        onShow: async (form) => {
            const purchaseForm = form;
            if (!purchaseForm) return;

            try {
                const [compRes, suppliersRes, productsRes] = await Promise.all([
                    serviceProvider.companies.getAll({ limit: 100 }),
                    serviceProvider.suppliers.getAll({ limit: 100 }),
                    serviceProvider.products.getAll({ limit: 100 })
                ]);

                if (compRes.success && compRes.data) {
                    populateSelect(purchaseForm.querySelector('select[name="company_id"]'), compRes.data.results || compRes.data);
                }

                if (suppliersRes.success && suppliersRes.data) {
                    populateSelect(purchaseForm.querySelector('select[name="supplier_id"]'), suppliersRes.data.results || suppliersRes.data);
                }

                if (productsRes.success && productsRes.data) {
                    const products = productsRes.data.results || productsRes.data;
                    purchaseForm._products = products;
                }
            } catch (e) {
            }

            // Configura detalles dinámicos de la compra
            const detailTemplate = `
                <tr class="purchase-detail-row">
                    <td><select name="product_id" class="form-input form-select no-choices"></select></td>
                    <td><input type="number" name="quantity" class="form-input" placeholder="Cantidad" min="1" value="0"></td>
                    <td><input type="number" name="unit_cost" class="form-input" placeholder="Costo" step="0.01"></td>
                    <td class="purchase-detail-subtotal">€ 0.00</td>
                    <td>
                        <button type="button" class="btn-remove-detail" title="Eliminar">
                            <span class="material-symbols-outlined">delete</span>
                        </button>
                    </td>
                </tr>
            `;
            setupDynamicDetails({
                containerId: 'purchase-details-tbody',
                btnAddId: 'btn-add-purchase-detail',
                template: detailTemplate,
                products: purchaseForm._products || [],
                onProductSelect: (product, row) => {
                    const costInput = row.querySelector('input[name="unit_cost"]');
                    if (costInput && product.purchase_price) {
                        costInput.value = product.purchase_price;
                    }
                    updateRowSubtotal(row);
                },
                isTableRow: true
            });

            // Actualiza el subtotal de una fila
            function updateRowSubtotal(row) {
                const costInput = row.querySelector('input[name="unit_cost"]');
                const qtyInput = row.querySelector('input[name="quantity"]');
                const subtotalCell = row.querySelector('.purchase-detail-subtotal');

                const cost = parseFloat(costInput?.value) || 0;
                const qty = parseInt(qtyInput?.value) || 0;
                const subtotal = qty * cost;
                subtotalCell.textContent = `€ ${subtotal.toFixed(2)}`;
                recalculateTotals();
            }

            // Recalcula los totales generales
            function recalculateTotals() {
                const rows = document.querySelectorAll('#purchase-details-tbody .purchase-detail-row');
                let grandSubtotal = 0;

                rows.forEach(row => {
                    const costInput = row.querySelector('input[name="unit_cost"]');
                    const qtyInput = row.querySelector('input[name="quantity"]');

                    const cost = parseFloat(costInput?.value) || 0;
                    const qty = parseInt(qtyInput?.value) || 0;

                    grandSubtotal += qty * cost;
                });

                const subtotalEl = document.getElementById('purchase-subtotal');
                const totalEl = document.getElementById('purchase-total');

                if (subtotalEl) subtotalEl.textContent = `€ ${grandSubtotal.toFixed(2)}`;
                if (totalEl) totalEl.textContent = `€ ${grandSubtotal.toFixed(2)}`;
            }

            document.getElementById('purchase-details-tbody')?.addEventListener('input', (e) => {
                const row = e.target.closest('.purchase-detail-row');
                if (row) updateRowSubtotal(row);
            });
        }
    });
}

// Maneja el envío del formulario de compra
async function handlePurchaseSubmit(e) {
    e.preventDefault();
    const form = e.target;

    const details = getRowsData('purchase-details-tbody', ['product_id', 'quantity', 'unit_cost'])
        .map(d => ({
            product_id: parseInt(d.product_id),
            quantity: parseInt(d.quantity),
            unit_cost: String(parseFloat(d.unit_cost))
        }))
        .filter(d => d.product_id && d.quantity > 0 && d.unit_cost > 0);

    if (details.length === 0) {
        toast.show('Debe agregar al menos un producto con cantidad y precio válidos', 'warning');
        return;
    }

    if (!form.company_id.value) {
        toast.show('Debe seleccionar una empresa', 'warning');
        return;
    }

    const data = {
        company_id: parseInt(form.company_id.value),
        supplier_id: parseInt(form.supplier_id.value),
        details: details
    };

    try {
        const response = await serviceProvider.purchases.create(data);
        if (response.success) {
            if (window.modal) window.modal.hide('modal-purchase');
            const modalEl = document.getElementById('modal-purchase');
            if (modalEl) modalEl.remove();

            await loadPurchasesData();
        } else {
            window.modal.showAlert('Atención', response.message || 'Error al crear compra', 'error');
        }
    } catch (error) {
        window.modal.showAlert('Atención', error.message || 'Error al crear compra', 'error');
    }
}

document.addEventListener('DOMContentLoaded', initPurchasesPage);
