// Lógica para la gestión de devoluciones de compras

import { toast } from '../components/Toast.js';
import { formatCurrency, formatDate, formatFullName } from '../utils/helpers.js';
import { serviceProvider } from '../services/ServiceProvider.js';
import { showModal, setupTableColumnToggles } from '../utils/base_page.js';
import { create, clearChildren, parseHTML, renderHTML } from '../utils/dom.js';
import { getFilterValues, initFilterListeners, loadFilterSelects } from '../utils/filter_utils.js';
import { DEFAULT_PAGINATION_LIMIT } from '../utils/const.js';
import { TemplateLoader } from '../utils/TemplateLoader.js';
import { TablePagination } from '../components/Pagination.js';
import { Table } from '../components/Table.js';

let purchaseReturnTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `<strong>#${item.id}</strong>` },
    {
        label: 'Compra Original',
        type: 'primary',
        value: (item) => `Compra #${item.purchase_id || (typeof item.purchase === 'object' && item.purchase ? item.purchase.id : item.purchase) || 'Desconocida'}`
    },
    { label: 'Total Devolución', type: 'normal', value: (item) => formatCurrency(item.total_amount || 0) },
    { label: 'Razón', type: 'normal', value: (item) => item.reason || '-' },
    { label: 'Estado', type: 'normal', value: (item) => `<span class="badge ${item.state === 'COMPLETED' ? 'badge-success' : 'badge-danger'}">${item.state === 'COMPLETED' ? 'Completada' : 'Cancelada'}</span>` },
    { label: 'Creado en', type: 'normal', value: (item) => item.created_at ? formatDate(item.created_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Actualizado en', type: 'normal', value: (item) => item.updated_at ? formatDate(item.updated_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Eliminado en', type: 'normal', value: (item) => item.deleted_at ? formatDate(item.deleted_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Creado por', type: 'audit', value: (item) => item.created_by?.first_name ? formatFullName(item.created_by) : (item.created_by?.email || '-') },
    { label: 'Actualizado por', type: 'audit', value: (item) => item.updated_by?.first_name ? formatFullName(item.updated_by) : (item.updated_by?.email || '-') },
    { label: 'Eliminado por', type: 'audit', value: (item) => item.deleted_by?.first_name ? formatFullName(item.deleted_by) : (item.deleted_by?.email || '-') }
];

// Muestra el modal con el detalle de una devolución de compra
async function handleShowPurchaseReturnDetail(pr) {
    const existingModal = document.getElementById('modal-purchase-return-detail');
    if (existingModal) existingModal.remove();

    const templateHtml = await TemplateLoader.load('purchase_return_detail');
    const container = create('div');
    container.appendChild(parseHTML(templateHtml));
    document.body.appendChild(container.firstElementChild);

    document.getElementById('purchase-return-detail-id').textContent = `#${pr.id}`;
    document.getElementById('purchase-return-detail-purchase').textContent = pr.purchase ? (pr.purchase.id ? `Compra #${pr.purchase.id}` : 'Compra desconocida') : `Compra #${pr.purchase_id || 'Desconocida'}`;
    document.getElementById('purchase-return-detail-date').textContent = formatDate(pr.created_at, 'dd/mm/yyyy HH:mm');
    document.getElementById('purchase-return-detail-reason').textContent = pr.reason || '-';
    document.getElementById('purchase-return-detail-total').textContent = formatCurrency(pr.total_amount || 0);

    const stateEl = document.getElementById('purchase-return-detail-state');
    stateEl.className = pr.state === 'COMPLETED' ? 'badge badge-success' : 'badge badge-danger';
    stateEl.textContent = pr.state === 'COMPLETED' ? 'Completada' : 'Cancelada';

    const tbody = document.getElementById('purchase-return-detail-tbody');
    tbody.innerHTML = '<tr><td colspan="4" class="text-center"><div class="spinner spinner-sm"></div></td></tr>';

    window.modal.show('modal-purchase-return-detail');

    try {
        const response = await serviceProvider.purchaseReturns.getDetailsPurchaseReturnById(pr.id);
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

// Inicializa la página de devoluciones de compras
async function initPurchaseReturnsPage() {
    if (window.sidebar) {
        window.sidebar.init('purchase_returns.html');
    }

    setupPurchaseReturnsPageHeader();

    purchaseReturnTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
        actions: {
            customHtml: (item) => `
                <div class="table-actions">
                    <button class="btn-action btn-view-detail" title="Ver Detalle">
                        <span class="material-symbols-outlined">visibility</span>
                    </button>
                    ${item.state === 'COMPLETED' ? `
                    <button class="btn-action btn-action-danger btn-cancel-pr" title="Anular Devolución">
                        <span class="material-symbols-outlined">cancel</span>
                    </button>
                    ` : '<span style="color: rgba(206,232,242,0.3); font-size: 12px;">—</span>'}
                </div>
            `,
            setupEvents: (tr, item) => {
                const btnView = tr.querySelector('.btn-view-detail');
                if (btnView) btnView.addEventListener('click', () => handleShowPurchaseReturnDetail(item));
                const btnCancel = tr.querySelector('.btn-cancel-pr');
                if (btnCancel) {
                    btnCancel.addEventListener('click', () => handleCancelPurchaseReturn(item));
                }
            }
        }
    });

    setupTableColumnToggles();

    // Cargar opciones de compras en el select de filtros
    await loadFilterSelects(['purchase-return-filter-purchase-id']);

    await loadPurchaseReturnsData();

    initFilterListeners('.card', async () => {
        await loadPurchaseReturnsData();
    });
}

// Configura el encabezado de la página
function setupPurchaseReturnsPageHeader() {
    const btnNew = create('button', 'btn btn-primary', { id: 'btn-new-purchase-return' });
    btnNew.appendChild(create('span', 'material-symbols-outlined', {}, 'add'));
    btnNew.appendChild(document.createTextNode('Nueva Devolución'));

    btnNew.addEventListener('click', () => handleShowPurchaseReturnModal());

    if (window.pageHeader) {
        window.pageHeader.init('Compras: Devoluciones', { extraActions: btnNew });
    }
}

// Carga los datos de las devoluciones de compras
async function loadPurchaseReturnsData() {
    purchaseReturnTable.showLoading();

    try {
        const filters = {
            limit: 100,
            ...getFilterValues('.card')
        };

        const response = await serviceProvider.purchaseReturns.getAll(filters);
        if (response.success && response.data) {
            const items = response.data.results || (Array.isArray(response.data) ? response.data : []);

            const paginator = new TablePagination(items, DEFAULT_PAGINATION_LIMIT, (pagedData) => {
                purchaseReturnTable.setData(pagedData);
            });

            paginator.init();
            purchaseReturnTable.setData(paginator.getCurrentPageData());
        } else {
		    toast.show(response.message || 'Error al cargar devoluciones', 'error');
		    purchaseReturnTable.setData([]);
		}
    } catch (error) {
        toast.show('No se pudo cargar la información de devoluciones. ' + (error.message || ''), 'error');
        purchaseReturnTable.setData([]);
    }
}

// Anula una devolución de compra
async function handleCancelPurchaseReturn(pr) {
    window.modal.showConfirm(
        'Anular Devolución',
        `¿Estás seguro de que deseas anular la devolución originada desde Compra #${pr.purchase_id || (typeof pr.purchase === 'object' ? pr.purchase.id : pr.purchase) || 'Desconocida'}?`,
        async () => {
            try {
                const response = await serviceProvider.purchaseReturns.cancel(pr.id);
                if (response.success) {
                    await loadPurchaseReturnsData();
                    toast.show('Devolución de compra anulada', 'success');
                } else {
                    window.modal.showAlert('Error', response.message || 'No se pudo anular la devolución', 'error');
                }
            } catch (error) {
                window.modal.showAlert('Error', error.message || 'Error al anular la devolución', 'error');
            }
        }
    );
}

// Muestra el modal para crear una devolución de compra
async function handleShowPurchaseReturnModal() {
    await showModal({
        modalId: 'modal-purchase-return',
        template: 'purchase_return',
        formId: 'form-purchase-return',
        singularName: 'Devolución de Compra',
        onSubmit: handlePurchaseReturnSubmit,
        onShow: async (form, item) => {
            const prForm = form;
            if (!prForm) return;

            try {
                const purchaseRes = await serviceProvider.purchases.getAll({ limit: 500, state: 'COMPLETED' });
                if (purchaseRes.success && purchaseRes.data) {
                    const purchases = purchaseRes.data.results || purchaseRes.data;
                    const selectPurchase = prForm.querySelector('select[name="purchase"]');

                    import('../utils/form_utils.js').then(m => {
                        const purchaseItems = purchases.map(p => ({
                            ...p,
                            displayName: `Compra #${p.id} (€${parseFloat(p.total_amount || 0).toFixed(2)})`
                        }));
                        m.populateSelect(selectPurchase, purchaseItems, 'displayName');
                        selectPurchase.dispatchEvent(new Event('change', { bubbles: true }));
                    });

                    // Carga productos al seleccionar una compra
                    selectPurchase.addEventListener('change', async (ev) => {
                        const purchaseId = ev.target.value;
                        const detailsContainer = document.getElementById('purchase-details-container');
                        if (!detailsContainer) return;
                        renderHTML(detailsContainer, '<p class="text-sm">Cargando productos...</p>');
                        if (!purchaseId) {
                            clearChildren(detailsContainer);
                            return;
                        }

                        try {
                            const res = await serviceProvider.purchases.getDetailsPurchaseById(purchaseId);
                            if (res.success && res.data) {
                                const details = res.data.results || res.data;
                                if (details.length === 0) {
                                    renderHTML(detailsContainer, '<p class="text-sm" style="color:red;">No hay productos detallados en esta compra.</p>');
                                    return;
                                }

                                renderHTML(detailsContainer, '<h5 style="margin-bottom:8px; font-size:14px;">Seleccione los productos a devolver:</h5>');
                                details.forEach(d => {
                                    const row = document.createElement('div');
                                    row.className = 'return-item-row';
                                    row.style.display = 'flex';
                                    row.style.alignItems = 'center';
                                    row.style.gap = '10px';
                                    row.style.marginBottom = '8px';

                                    const productName = typeof d.product === 'object' ? d.product.name : `Producto #${d.product_id || d.product}`;
                                    const prodId = d.product_id || (typeof d.product === 'object' ? d.product.id : d.product);
                                    const unitCost = d.unit_cost || 0;
                                    const maxQty = d.quantity || 1;

                                    renderHTML(row, `
                                        <input type="checkbox" class="return-detail-check" data-product-id="${prodId}" data-unit-cost="${unitCost}">
                                        <label style="flex:1; font-size:14px;">${productName} (Máx: ${maxQty})</label>
                                        <input type="number" class="form-input return-detail-qty" min="1" max="${maxQty}" value="1" disabled style="width: 80px; padding: 4px;">
                                    `);
                                    const check = row.querySelector('.return-detail-check');
                                    const qtyInput = row.querySelector('.return-detail-qty');
                                    check.addEventListener('change', () => qtyInput.disabled = !check.checked);
                                    detailsContainer.appendChild(row);
                                });
                            }
                        } catch (err) {
                            renderHTML(detailsContainer, '<p class="text-sm" style="color:red;">Error al cargar detalles.</p>');
                        }
                    });
                }
            } catch (e) {
            }
        }
    });
}

// Maneja el envío del formulario de devolución de compra
async function handlePurchaseReturnSubmit(e) {
    e.preventDefault();
    const form = e.target;

    // Formato anidado de Devolución de Compras con detalles
    const data = {
        purchase_id: parseInt(form.purchase.value),
        reason: form.reason.value,
        details: []
    };

    const checkedItems = form.querySelectorAll('.return-detail-check:checked');
    checkedItems.forEach(check => {
        const row = check.parentElement;
        const qtyInput = row.querySelector('.return-detail-qty');
        const originalCost = parseFloat(check.dataset.unitCost);

        data.details.push({
            product_id: parseInt(check.dataset.productId),
            quantity: parseInt(qtyInput.value),
            unit_cost: Math.abs(originalCost).toFixed(2)
        });
    });

    if (data.details.length === 0) {
        toast.show('Debe seleccionar al menos un producto para devolver.', 'warning');
        return;
    }

    try {
        const response = await serviceProvider.purchaseReturns.create(data);
        if (response.success) {
            if (window.modal) window.modal.hide('modal-purchase-return');
            const modalEl = document.getElementById('modal-purchase-return');
            if (modalEl) modalEl.remove();

            await loadPurchaseReturnsData();
        } else {
            window.modal.showAlert('Atención', response.message || 'Error al crear la devolución', 'error');
        }
    } catch (error) {
        window.modal.showAlert('Atención', error.message || 'Error al crear la devolución', 'error');
    }
}

document.addEventListener('DOMContentLoaded', initPurchaseReturnsPage);
