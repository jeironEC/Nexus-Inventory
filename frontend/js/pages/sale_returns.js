// Lógica para la gestión de devoluciones de ventas

import { toast } from '../components/Toast.js';
import { formatCurrency, formatDate, formatFullName } from '../utils/helpers.js';
import { serviceProvider } from '../services/ServiceProvider.js';
import { showModal, setupTableColumnToggles } from '../utils/base_page.js';
import { create, clearChildren, renderHTML } from '../utils/dom.js';
import { getFilterValues, initFilterListeners, loadFilterSelects } from '../utils/filter_utils.js';
import { DEFAULT_PAGINATION_LIMIT } from '../utils/const.js';
import { TablePagination } from '../components/Pagination.js';
import { Table } from '../components/Table.js';

let saleReturnTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `<strong>#${item.id}</strong>` },
    {
        label: 'Venta Original',
        type: 'primary',
        value: (item) => `Venta #${item.sale_id || (typeof item.sale === 'object' && item.sale ? item.sale.id : item.sale) || 'Desconocida'}`
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

// Inicializa la página de devoluciones de ventas
async function initSaleReturnsPage() {
    if (window.sidebar) {
        window.sidebar.init('sale_returns.html');
    }

    setupSaleReturnsPageHeader();

    saleReturnTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
        actions: {
            customHtml: (item) => `
                <div class="table-actions">
                    ${item.state === 'COMPLETED' ? `
                    <button class="btn-action btn-action-danger btn-cancel-sr" title="Anular Devolución">
                        <span class="material-symbols-outlined">cancel</span>
                    </button>
                    ` : '<span style="color: rgba(206,232,242,0.3); font-size: 12px;">—</span>'}
                </div>
            `,
            setupEvents: (tr, item) => {
                const btnCancel = tr.querySelector('.btn-cancel-sr');
                if (btnCancel) {
                    btnCancel.addEventListener('click', () => handleCancelSaleReturn(item));
                }
            }
        }
    });

    setupTableColumnToggles();

    // Cargar opciones de ventas en el select de filtros
    await loadFilterSelects(['sale-return-filter-sale-id']);

    await loadSaleReturnsData();

    initFilterListeners('.card', async () => {
        await loadSaleReturnsData();
    });
}

// Configura el encabezado de la página
function setupSaleReturnsPageHeader() {
    const btnNew = create('button', 'btn btn-primary', { id: 'btn-new-sale-return' });
    btnNew.appendChild(create('span', 'material-symbols-outlined', {}, 'add'));
    btnNew.appendChild(document.createTextNode('Nueva Devolución'));

    btnNew.addEventListener('click', () => handleShowSaleReturnModal());

    if (window.pageHeader) {
        window.pageHeader.init('Ventas: Devoluciones', { extraActions: btnNew });
    }
}

// Carga los datos de las devoluciones de ventas
async function loadSaleReturnsData() {
    saleReturnTable.showLoading();

    try {
        const filters = {
            limit: 100,
            ...getFilterValues('.card')
        };

        const response = await serviceProvider.saleReturns.getAll(filters);
        if (response.success && response.data) {
            const items = response.data.results || (Array.isArray(response.data) ? response.data : []);

            const paginator = new TablePagination(items, DEFAULT_PAGINATION_LIMIT, (pagedData) => {
                saleReturnTable.setData(pagedData);
            });

            paginator.init();
            saleReturnTable.setData(paginator.getCurrentPageData());
        }
    } catch (error) {
        saleReturnTable.showError('No se pudo cargar la información de devoluciones. ' + (error.message || ''));
    }
}

// Anula una devolución de venta
async function handleCancelSaleReturn(sr) {
    window.modal.showConfirm(
        'Anular Devolución',
        `¿Estás seguro de que deseas anular la devolución originada desde Venta #${sr.sale_id || (typeof sr.sale === 'object' ? sr.sale.id : sr.sale) || 'Desconocida'}?`,
        async () => {
            try {
                const response = await serviceProvider.saleReturns.cancel(sr.id);
                if (response.success) {
                    await loadSaleReturnsData();
                    toast.show('Devolución de venta anulada', 'success');
                } else {
                    window.modal.showAlert('Error', response.message || 'No se pudo anular la devolución', 'error');
                }
            } catch (error) {
                window.modal.showAlert('Error', error.message || 'Error al anular la devolución', 'error');
            }
        }
    );
}

// Muestra el modal para crear una devolución de venta
async function handleShowSaleReturnModal() {
    await showModal({
        modalId: 'modal-sale-return',
        template: 'sale_return',
        formId: 'form-sale-return',
        singularName: 'Devolución de Venta',
        onSubmit: handleSaleReturnSubmit,
        onShow: async (form, item) => {
            const srForm = form;
            if (!srForm) return;

            try {
                const saleRes = await serviceProvider.sales.getAll({ limit: 500, state: 'COMPLETED' });
                if (saleRes.success && saleRes.data) {
                    const sales = saleRes.data.results || saleRes.data;
                    const selectSale = srForm.querySelector('select[name="sale"]');

                    import('../utils/form_utils.js').then(m => {
                        // Transformar datos para mostrar formato específico
                        const saleItems = sales.map(s => ({
                            ...s,
                            displayName: `Venta #${s.id} (€${parseFloat(s.total_amount || 0).toFixed(2)})`
                        }));
                        m.populateSelect(selectSale, saleItems, 'displayName');
                        selectSale.dispatchEvent(new Event('change', { bubbles: true }));
                    });

                    // Carga productos al seleccionar una venta
                    selectSale.addEventListener('change', async (ev) => {
                        const saleId = ev.target.value;
                        const detailsContainer = document.getElementById('sale-details-container');
                        if (!detailsContainer) return;
                        renderHTML(detailsContainer, '<p class="text-sm">Cargando productos...</p>');
                        if (!saleId) {
                            clearChildren(detailsContainer);
                            return;
                        }

                        try {
                            const res = await serviceProvider.sales.getDetailsSaleById(saleId);
                            if (res.success && res.data) {
                                const details = res.data.results || res.data;
                                if (details.length === 0) {
                                    renderHTML(detailsContainer, '<p class="text-sm" style="color:red;">No hay productos detallados en esta venta.</p>');
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
                                    const unitPrice = d.unit_price || 0;
                                    const maxQty = d.quantity || 1;

                                    renderHTML(row, `
                                        <input type="checkbox" class="return-detail-check" data-product-id="${prodId}" data-unit-price="${unitPrice}">
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

// Maneja el envío del formulario de devolución de venta
async function handleSaleReturnSubmit(e) {
    e.preventDefault();
    const form = e.target;

    // Formato anidado de Devolución de Ventas con detalles
    const data = {
        sale_id: parseInt(form.sale.value),
        reason: form.reason.value,
        details: []
    };

    const checkedItems = form.querySelectorAll('.return-detail-check:checked');
    checkedItems.forEach(check => {
        const row = check.parentElement;
        const qtyInput = row.querySelector('.return-detail-qty');
        const originalPrice = parseFloat(check.dataset.unitPrice);

        data.details.push({
            product_id: parseInt(check.dataset.productId),
            quantity: parseInt(qtyInput.value),
            unit_price: Math.abs(originalPrice).toFixed(2)
        });
    });

    if (data.details.length === 0) {
        toast.show('Debe seleccionar al menos un producto para devolver.', 'warning');
        return;
    }

    try {
        const response = await serviceProvider.saleReturns.create(data);
        if (response.success) {
            if (window.modal) window.modal.hide('modal-sale-return');
            const modalEl = document.getElementById('modal-sale-return');
            if (modalEl) modalEl.remove();

            await loadSaleReturnsData();
        } else {
            window.modal.showAlert('Atención', response.message || 'Error al crear la devolución', 'error');
        }
    } catch (error) {
        window.modal.showAlert('Atención', error.message || 'Error al crear la devolución', 'error');
    }
}

document.addEventListener('DOMContentLoaded', initSaleReturnsPage);
