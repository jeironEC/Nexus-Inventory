// Lógica para la gestión de productos

import { serviceProvider } from '../services/ServiceProvider.js';
import { initPage, loadData, handleToggle, showModal, handleSubmit, createNewButton } from '../utils/base_page.js';
import { formatDate, formatFullName, formatCurrency } from '../utils/helpers.js';
import { Table } from '../components/Table.js';

const CONFIG = {
    pageName: 'Productos',
    htmlFile: 'products.html',
    service: serviceProvider.products,
    singularName: 'producto',
    modalId: 'modal-product',
    formId: 'form-product',
    template: 'product',
    tableBodySelector: '.table tbody',
    filterSelectIds: ['product-filter-category-id']
};

let productTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `#${item.id}` },
    { label: 'Categoría', type: 'normal', value: (item) => item.category?.name || '-' },
    { label: 'Nombre', type: 'primary', value: (item) => item.name },
    { label: 'Descripción', type: 'normal', value: (item) => item.description || '-' },
    { label: 'Código Único', type: 'primary', value: (item) => item.unique_code || '-' },
    { label: 'Precio Compra', type: 'normal', value: (item) => formatCurrency(item.purchase_price) },
    { label: 'Precio Venta', type: 'normal', value: (item) => formatCurrency(item.sale_price) },
    { label: 'Descuento (%)', type: 'normal', value: (item) => `${parseFloat(item.discount_percentage || 0)}%` },
    { label: 'Estado', type: 'normal', value: (item) => `<span class="badge ${item.is_active ? 'badge-success' : 'badge-danger'}">${item.is_active ? 'Activo' : 'Inactivo'}</span>` },
    { label: 'Creado en', type: 'normal', value: (item) => item.created_at ? formatDate(item.created_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Actualizado en', type: 'normal', value: (item) => item.updated_at ? formatDate(item.updated_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Eliminado en', type: 'normal', value: (item) => item.deleted_at ? formatDate(item.deleted_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Creado por', type: 'audit', value: (item) => item.created_by?.first_name ? formatFullName(item.created_by) : (item.created_by?.email || '-') },
    { label: 'Actualizado por', type: 'audit', value: (item) => item.updated_by?.first_name ? formatFullName(item.updated_by) : (item.updated_by?.email || '-') },
    { label: 'Eliminado por', type: 'audit', value: (item) => item.deleted_by?.first_name ? formatFullName(item.deleted_by) : (item.deleted_by?.email || '-') }
];

// Inicializa la página de productos
async function initProductsPage() {
    const btnNew = createNewButton('btn-new-product', 'Nuevo Producto', () => handleShowProductModal());

    productTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
        actions: {
            onEdit: handleShowProductModal,
            onToggle: (item) => handleToggle({
                item,
                service: CONFIG.service,
                loadFn: loadProductsData,
                singularName: CONFIG.singularName
            })
        }
    });

    await initPage({
        ...CONFIG,
        extraActions: btnNew,
        onLoadData: loadProductsData
    });
}

// Carga los datos de los productos
async function loadProductsData() {
    await loadData({
        service: CONFIG.service,
        renderFn: (data) => productTable.setData(data)
    });
}

// Muestra el modal para crear o editar un producto
function handleShowProductModal(product = null) {
    showModal({
        ...CONFIG,
        item: product,
        onShow: async (form) => {
            try {
                const catRes = await serviceProvider.categories.getAll({ limit: 100 });
                if (catRes.success && catRes.data) {
                    const cats = catRes.data.results || catRes.data;
                    const select = form.querySelector('select[name="category"]');
                    import('../utils/form_utils.js').then(m => {
                        const selectedVal = (product && product.category) ? product.category.id : null;
                        m.populateSelect(select, cats, 'name', 'id', selectedVal);
                    });
                }
            } catch(e) {
            }
        },
        onSubmit: async (e, form) => {
            const data = {
                name: form.name.value,
                category_id: form.category.value,
                unique_code: form.unique_code.value,
                description: form.description.value,
                sale_price: form.sale_price.value,
                purchase_price: form.purchase_price.value,
                discount_percentage: form.discount_percentage.value
            };

            await handleSubmit(e, {
                service: CONFIG.service,
                modalId: CONFIG.modalId,
                loadFn: loadProductsData,
                singularName: CONFIG.singularName,
                customData: data
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', initProductsPage);
