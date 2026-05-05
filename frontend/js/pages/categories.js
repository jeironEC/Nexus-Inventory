// Gestión de categorías del inventario

import { serviceProvider } from '../services/ServiceProvider.js';
import { initPage, loadData, handleToggle, showModal, handleSubmit, createNewButton } from '../utils/base_page.js';
import { formatDate, formatFullName } from '../utils/helpers.js';
import { Table } from '../components/Table.js';

const CONFIG = {
    pageName: 'Categorías',
    htmlFile: 'categories.html',
    service: serviceProvider.categories,
    singularName: 'categoría',
    modalId: 'modal-category',
    formId: 'form-category',
    template: 'category',
    tableBodySelector: '.table tbody'
};

let categoryTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `#${item.id}` },
    { label: 'Nombre', type: 'primary', value: (item) => item.name },
    { label: 'Descripción', type: 'normal', value: (item) => item.description || '-' },
    { label: 'Estado', type: 'normal', value: (item) => `<span class="badge ${item.is_active ? 'badge-success' : 'badge-danger'}">${item.is_active ? 'Activo' : 'Inactivo'}</span>` },
    { label: 'Creado en', type: 'normal', value: (item) => item.created_at ? formatDate(item.created_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Actualizado en', type: 'normal', value: (item) => item.updated_at ? formatDate(item.updated_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Eliminado en', type: 'normal', value: (item) => item.deleted_at ? formatDate(item.deleted_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Creado por', type: 'audit', value: (item) => item.created_by?.first_name ? formatFullName(item.created_by) : (item.created_by?.email || '-') },
    { label: 'Actualizado por', type: 'audit', value: (item) => item.updated_by?.first_name ? formatFullName(item.updated_by) : (item.updated_by?.email || '-') },
    { label: 'Eliminado por', type: 'audit', value: (item) => item.deleted_by?.first_name ? formatFullName(item.deleted_by) : (item.deleted_by?.email || '-') }
];

// Inicializa la página de categorías
async function initCategoriesPage() {
    const btnNew = createNewButton('btn-new-category', 'Nueva Categoría', () => handleShowCategoryModal());

    categoryTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
        actions: {
            onEdit: handleShowCategoryModal,
            onToggle: (item) => handleToggle({
                item,
                service: CONFIG.service,
                loadFn: loadCategoriesData,
                singularName: CONFIG.singularName
            })
        }
    });

    await initPage({
        ...CONFIG,
        extraActions: btnNew,
        onLoadData: loadCategoriesData
    });
}

// Carga los datos de las categorías
async function loadCategoriesData() {
    await loadData({
        service: CONFIG.service,
        renderFn: (data) => categoryTable.setData(data)
    });
}

// Muestra el modal para crear o editar una categoría
function handleShowCategoryModal(category = null) {
    showModal({
        ...CONFIG,
        item: category,
        onSubmit: async (e, form) => {
            await handleSubmit(e, {
                service: CONFIG.service,
                modalId: CONFIG.modalId,
                loadFn: loadCategoriesData,
                singularName: CONFIG.singularName
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', initCategoriesPage);
