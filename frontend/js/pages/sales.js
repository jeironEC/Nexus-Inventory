// Lógica para la gestión de ventas

import { toast } from '../components/Toast.js';
import { serviceProvider } from '../services/ServiceProvider.js';
import { create, parseHTML } from '../utils/dom.js';
import { initFilterListeners, loadFilterSelects } from '../utils/filter_utils.js';
import { loadData, showModal, setupTableColumnToggles } from '../utils/base_page.js';
import { formatCurrency, formatDate, formatFullName } from '../utils/helpers.js';
import { setupDynamicDetails, getRowsData, populateSelect } from '../utils/form_utils.js';
import { TemplateLoader } from '../utils/TemplateLoader.js';
import { Table } from '../components/Table.js';

let saleTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `#${item.id}` },
    { label: 'Cliente', type: 'primary', value: (item) => item.customer?.first_name ? `${item.customer.first_name} ${item.customer.last_name || ''}`.trim() : 'Anónimo' },
    { label: 'Descuento', type: 'normal', value: (item) => formatCurrency(item.discount_amount) },
    { label: 'Subtotal', type: 'normal', value: (item) => formatCurrency(item.subtotal) },
    { label: 'Impuesto (%)', type: 'normal', value: (item) => `${parseFloat(item.tax_percentage || 0)}%` },
    { label: 'Total Impuesto', type: 'normal', value: (item) => formatCurrency(item.tax_amount) },
    { label: 'Total', type: 'normal', value: (item) => formatCurrency(item.total_amount) },
    { label: 'Método Pago', type: 'normal', value: (item) => ({ CASH: 'Efectivo', CARD: 'Tarjeta', TRANSFER: 'Transferencia' }[item.payment_method] || item.payment_method || '-') },
    { label: 'Estado', type: 'normal', value: (item) => `<span class="badge ${item.state === 'COMPLETED' ? 'badge-success' : 'badge-danger'}">${item.state === 'COMPLETED' ? 'Completada' : 'Cancelada'}</span>` },
    { label: 'Creado en', type: 'normal', value: (item) => item.created_at ? formatDate(item.created_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Actualizado en', type: 'normal', value: (item) => item.updated_at ? formatDate(item.updated_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Eliminado en', type: 'normal', value: (item) => item.deleted_at ? formatDate(item.deleted_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Creado por', type: 'audit', value: (item) => item.user?.first_name ? formatFullName(item.user) : (item.user?.email || '-') },
    { label: 'Actualizado por', type: 'audit', value: (item) => item.updated_by?.first_name ? formatFullName(item.updated_by) : (item.updated_by?.email || '-') },
    { label: 'Eliminado por', type: 'audit', value: (item) => item.deleted_by?.first_name ? formatFullName(item.deleted_by) : (item.deleted_by?.email || '-') }
];

// Muestra el modal con el detalle de una venta
async function handleShowSaleDetail(sale) {
    const existingModal = document.getElementById('modal-sale-detail');
    if (existingModal) existingModal.remove();

    const templateHtml = await TemplateLoader.load('sale_detail');
    const container = create('div');
    container.appendChild(parseHTML(templateHtml));
    document.body.appendChild(container.firstElementChild);

    document.getElementById('sale-detail-id').textContent = `#${sale.id}`;
    document.getElementById('sale-detail-customer').textContent = sale.customer?.first_name ? `${sale.customer.first_name} ${sale.customer.last_name || ''}`.trim() : 'Anónimo';
    document.getElementById('sale-detail-date').textContent = formatDate(sale.created_at, 'dd/mm/yyyy HH:mm');
    document.getElementById('sale-detail-payment').textContent = ({ CASH: 'Efectivo', CARD: 'Tarjeta', TRANSFER: 'Transferencia' }[sale.payment_method] || sale.payment_method || '-');
    document.getElementById('sale-detail-discount').textContent = formatCurrency(sale.discount_amount);
    document.getElementById('sale-detail-subtotal-summary').textContent = formatCurrency(sale.subtotal);
    document.getElementById('sale-detail-tax').textContent = formatCurrency(sale.tax_amount);
    document.getElementById('sale-detail-total').textContent = formatCurrency(sale.total_amount);

    const stateEl = document.getElementById('sale-detail-state');
    stateEl.className = sale.state === 'COMPLETED' ? 'badge badge-success' : 'badge badge-danger';
    stateEl.textContent = sale.state === 'COMPLETED' ? 'Completada' : 'Cancelada';

    const tbody = document.getElementById('sale-detail-tbody');
    tbody.innerHTML = '<tr><td colspan="4" class="text-center"><div class="spinner spinner-sm"></div></td></tr>';

    window.modal.show('modal-sale-detail');

    try {
        const response = await serviceProvider.sales.getDetailsSaleById(sale.id);
        if (response.success && response.data) {
            const items = response.data.results || response.data;
            tbody.innerHTML = items.map(item => `
                <tr>
                    <td>${item.product?.name || 'Producto desconocido'}</td>
                    <td>${item.quantity}</td>
                    <td>${formatCurrency(item.unit_price)}</td>
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

// Inicializa la página de ventas
async function initSalesPage() {
    if (window.sidebar) {
        window.sidebar.init('sales.html');
    }

    setupSalesPageHeader();

    saleTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
        actions: {
            customHtml: (item) => `
                <div class="table-actions">
                    <button class="btn-action btn-view-detail" title="Ver Detalle">
                        <span class="material-symbols-outlined">visibility</span>
                    </button>
                    ${item.state === 'COMPLETED' ? `
                    <button class="btn-action btn-action-danger btn-cancel-sale" title="Cancelar Venta">
                        <span class="material-symbols-outlined">cancel</span>
                    </button>` : '<span style="color: rgba(206,232,242,0.3); font-size: 12px;">—</span>'}
                </div>
            `,
            setupEvents: (tr, item) => {
                const btnView = tr.querySelector('.btn-view-detail');
                if (btnView) btnView.addEventListener('click', () => handleShowSaleDetail(item));
                const btnCancel = tr.querySelector('.btn-cancel-sale');
                if (btnCancel) btnCancel.addEventListener('click', () => handleCancelSale(item));
            }
        }
    });

    setupTableColumnToggles();

    await loadFilterSelects(['sale-filter-customer-id']);

    await loadSalesData();

    initFilterListeners('.card', async () => {
        await loadSalesData();
    });
}

// Carga los datos de las ventas
async function loadSalesData() {
    await loadData({
        service: serviceProvider.sales,
        renderFn: (data) => saleTable.setData(data)
    });
}

// Cancela una venta
async function handleCancelSale(sale) {
    window.modal.showConfirm(
        'Cancelar Venta',
        `¿Estás seguro de que deseas cancelar la venta #${sale.id}? Esta acción afectará el inventario según la configuración.`,
        async () => {
            try {
                const response = await serviceProvider.sales.cancel(sale.id);
                if (response.success) {
                    await loadSalesData();
                    toast.show('Venta cancelada exitosamente', 'success');
                } else {
                    window.modal.showAlert('Error', response.message || 'No se pudo cancelar la venta', 'error');
                }
            } catch (error) {
                window.modal.showAlert('Error', error.message || 'Error al cancelar la venta', 'error');
            }
        }
    );
}

// Configura el encabezado de la página
function setupSalesPageHeader() {
    const btnNew = create('button', 'btn btn-primary', { id: 'btn-new-sale' });
    btnNew.appendChild(create('span', 'material-symbols-outlined', {}, 'add'));
    btnNew.appendChild(document.createTextNode('Nueva Venta'));

    btnNew.addEventListener('click', () => handleShowSaleModal());

    if (window.pageHeader) {
        window.pageHeader.init('Ventas', { extraActions: btnNew });
    }
}

// Muestra el modal para crear una nueva venta
async function handleShowSaleModal() {
    await showModal({
        modalId: 'modal-sale',
        template: 'sale',
        formId: 'form-sale',
        singularName: 'Venta',
        onSubmit: handleSaleSubmit,
        onShow: async (form) => {
            const saleForm = form;
            if (!saleForm) return;

            try {
                const [compRes, custRes, prodRes] = await Promise.all([
                    serviceProvider.companies.getAll({ limit: 100 }),
                    serviceProvider.customers.getAll({ limit: 100 }),
                    serviceProvider.products.getAll({ limit: 100 })
                ]);

                if (compRes.success && compRes.data) {
                    populateSelect(saleForm.querySelector('select[name="company_id"]'), compRes.data.results || compRes.data);
                }

                if (custRes.success && custRes.data) {
                    populateSelect(saleForm.querySelector('select[name="customer_id"]'), custRes.data.results || custRes.data, 'full_name');
                }

                if (prodRes.success && prodRes.data) {
                    const allProducts = prodRes.data.results || prodRes.data;

                    // Obtener inventario de forma separada para no bloquear si falla
                    let invData = [];
                    try {
                        const invRes = await serviceProvider.inventories.getAll({ limit: 1000 });
                        if (invRes.success && invRes.data) {
                            invData = invRes.data.results || invRes.data;
                        }
                    } catch (e) {
                    }

                    if (invData.length > 0) {
                        // Crear mapa de stock por product_id
                        const stockMap = {};
                        invData.forEach(inv => {
                            const pid = inv.product?.id || inv.product_id;
                            if (pid) {
                                stockMap[pid] = Number(inv.quantity) || 0;
                            }
                        });

                        // Guardar stock en el form para validación
                        saleForm._stockMap = stockMap;

                        // Filtrar solo productos con stock > 0
                        saleForm._products = allProducts.filter(p => (stockMap[p.id] || 0) > 0);
                    } else {
                        saleForm._products = allProducts;
                    }
                }
            } catch (e) {
            }

            // Configura detalles dinámicos de la venta
            const detailTemplate = `
                <tr class="sale-detail-row">
                    <td><select name="product_id" class="form-input form-select no-choices"></select></td>
                    <td><input type="number" name="quantity" class="form-input" placeholder="0" min="1" value="0"></td>
                    <td><input type="number" name="unit_price" class="form-input" placeholder="0.00" step="0.01"></td>
                    <td><input type="number" name="discount_percentage" class="form-input" placeholder="0" min="0" max="100" value="0" step="1" readonly tabindex="-1"></td>
                    <td class="sale-detail-subtotal">€ 0.00</td>
                    <td>
                        <button type="button" class="btn-remove-detail" title="Eliminar">
                            <span class="material-symbols-outlined">delete</span>
                        </button>
                    </td>
                </tr>
            `;
            setupDynamicDetails({
                containerId: 'sale-details-tbody',
                btnAddId: 'btn-add-sale-detail',
                template: detailTemplate,
                products: saleForm._products || [],
                onProductSelect: (product, row) => {
                    const priceInput = row.querySelector('input[name="unit_price"]');
                    if (priceInput && product.sale_price) {
                        priceInput.value = product.sale_price;
                    }
                    const discountInput = row.querySelector('input[name="discount_percentage"]');
                    if (discountInput) {
                        discountInput.value = product.discount_percentage || 0;
                    }
                    const qtyInput = row.querySelector('input[name="quantity"]');
                    const stockMap = saleForm._stockMap || {};
                    const stock = stockMap[product.id] || 0;
                    if (qtyInput) {
                        qtyInput.max = stock;
                        if (parseInt(qtyInput.value) > stock) {
                            qtyInput.value = stock;
                        }
                    }
                    updateRowSubtotal(row);
                },
                isTableRow: true
            });

            // Actualiza el subtotal de una fila
            function updateRowSubtotal(row) {
                const priceInput = row.querySelector('input[name="unit_price"]');
                const qtyInput = row.querySelector('input[name="quantity"]');
                const discountInput = row.querySelector('input[name="discount_percentage"]');
                const subtotalCell = row.querySelector('.sale-detail-subtotal');

                const price = parseFloat(priceInput?.value) || 0;
                const qty = parseInt(qtyInput?.value) || 0;
                const discount = parseFloat(discountInput?.value) || 0;

                const priceAfterDiscount = price - (price * discount / 100);
                const subtotal = qty * priceAfterDiscount;
                subtotalCell.textContent = `€ ${subtotal.toFixed(2)}`;
                recalculateTotals();
            }

            // Recalcula los totales generales
            function recalculateTotals() {
                const rows = document.querySelectorAll('#sale-details-tbody .sale-detail-row');
                let grandSubtotal = 0;

                rows.forEach(row => {
                    const priceInput = row.querySelector('input[name="unit_price"]');
                    const qtyInput = row.querySelector('input[name="quantity"]');
                    const discountInput = row.querySelector('input[name="discount_percentage"]');

                    const price = parseFloat(priceInput?.value) || 0;
                    const qty = parseInt(qtyInput?.value) || 0;
                    const discount = parseFloat(discountInput?.value) || 0;

                    const priceAfterDiscount = price - (price * discount / 100);
                    grandSubtotal += qty * priceAfterDiscount;
                });

                const taxPercentage = parseFloat(saleForm.tax_percentage?.value) || 21;
                const taxAmount = grandSubtotal * taxPercentage / 100;
                const grandTotal = grandSubtotal + taxAmount;

                const subtotalEl = document.getElementById('sale-subtotal');
                const taxEl = document.getElementById('sale-tax');
                const totalEl = document.getElementById('sale-total');

                if (subtotalEl) subtotalEl.textContent = `€ ${grandSubtotal.toFixed(2)}`;
                if (taxEl) taxEl.textContent = `€ ${taxAmount.toFixed(2)}`;
                if (totalEl) totalEl.textContent = `€ ${grandTotal.toFixed(2)}`;
            }

            document.getElementById('sale-details-tbody')?.addEventListener('input', (e) => {
                const row = e.target.closest('.sale-detail-row');
                if (row) updateRowSubtotal(row);
            });
        }
    });
}

// Maneja el envío del formulario de venta
async function handleSaleSubmit(e) {
    e.preventDefault();
    const form = e.target;

    const stockMap = form._stockMap || {};

    const details = getRowsData('sale-details-tbody', ['product_id', 'quantity', 'unit_price'])
        .map(d => ({
            product_id: parseInt(d.product_id),
            quantity: parseInt(d.quantity),
            unit_price: parseFloat(d.unit_price)
        }))
        .filter(d => d.product_id && d.quantity > 0 && d.unit_price > 0);

    if (details.length === 0) {
        toast.show('Debe agregar al menos un producto con cantidad y precio válidos', 'warning');
        return;
    }

    // Validar stock por producto
    for (const d of details) {
        const available = stockMap[d.product_id] || 0;
        if (d.quantity > available) {
            const product = (form._products || []).find(p => p.id === d.product_id);
            const name = product?.name || `Producto #${d.product_id}`;
            toast.show(`Stock insuficiente para "${name}". Disponible: ${available}`, 'error');
            return;
        }
    }

    if (!form.company_id.value) {
        toast.show('Debe seleccionar una empresa', 'warning');
        return;
    }

    if (!form.payment_method.value) {
        toast.show('Debe seleccionar un método de pago', 'warning');
        return;
    }

    const validPaymentMethods = ['CASH', 'CARD', 'TRANSFER'];
    if (!validPaymentMethods.includes(form.payment_method.value)) {
        toast.show('Método de pago no válido', 'warning');
        return;
    }

    const customerId = form.customer_id.value ? parseInt(form.customer_id.value) : null;

    const data = {
        company_id: parseInt(form.company_id.value),
        customer_id: customerId,
        payment_method: form.payment_method.value,
        tax_percentage: String(form.tax_percentage.value || 21),
        details: details.map(d => ({
            product_id: d.product_id,
            quantity: d.quantity,
            unit_price: String(d.unit_price)
        }))
    };

    try {
        const response = await serviceProvider.sales.create(data);
        if (response.success) {
            if (window.modal) window.modal.hide('modal-sale');
            const modalEl = document.getElementById('modal-sale');
            if (modalEl) modalEl.remove();

            await loadSalesData();
        } else {
            window.modal.showAlert('Atención', response.message || 'Error al crear venta', 'error');
        }
    } catch (error) {
        window.modal.showAlert('Atención', error.message || 'Error al crear venta', 'error');
    }
}

document.addEventListener('DOMContentLoaded', initSalesPage);
