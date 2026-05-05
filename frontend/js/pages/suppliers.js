// Lógica para la gestión de proveedores

import { serviceProvider } from '../services/ServiceProvider.js';
import { initPage, loadData, handleToggle, showModal, handleSubmit, createNewButton } from '../utils/base_page.js';
import { formatDate, formatFullName } from '../utils/helpers.js';
import { Table } from '../components/Table.js';

const CONFIG = {
    pageName: 'Proveedores',
    htmlFile: 'suppliers.html',
    service: serviceProvider.suppliers,
    singularName: 'proveedor',
    modalId: 'modal-supplier',
    formId: 'form-supplier',
    template: 'supplier',
    tableBodySelector: '.table tbody'
};

let supplierTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `#${item.id}` },
    { label: 'Nombre', type: 'primary', value: (item) => item.name },
    { label: 'Email', type: 'normal', value: (item) => item.email || '-' },
    { label: 'NIF', type: 'normal', value: (item) => item.nif || '-' },
    { label: 'Teléfono', type: 'normal', value: (item) => item.number_phone || '-' },
    { label: 'Dirección', type: 'normal', value: (item) => item.address || '-' },
    { label: 'Estado', type: 'normal', value: (item) => `<span class="badge ${item.is_active ? 'badge-success' : 'badge-danger'}">${item.is_active ? 'Activo' : 'Inactivo'}</span>` },
    { label: 'Creado en', type: 'normal', value: (item) => item.created_at ? formatDate(item.created_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Actualizado en', type: 'normal', value: (item) => item.updated_at ? formatDate(item.updated_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Eliminado en', type: 'normal', value: (item) => item.deleted_at ? formatDate(item.deleted_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Creado por', type: 'audit', value: (item) => item.created_by?.first_name ? formatFullName(item.created_by) : (item.created_by?.email || '-') },
    { label: 'Actualizado por', type: 'audit', value: (item) => item.updated_by?.first_name ? formatFullName(item.updated_by) : (item.updated_by?.email || '-') },
    { label: 'Eliminado por', type: 'audit', value: (item) => item.deleted_by?.first_name ? formatFullName(item.deleted_by) : (item.deleted_by?.email || '-') }
];

// Inicializa la página de proveedores
async function initSuppliersPage() {
    const btnNew = createNewButton('btn-new-supplier', 'Nuevo Proveedor', () => handleShowSupplierModal());

    supplierTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
        actions: {
            onEdit: handleShowSupplierModal,
            onToggle: (item) => handleToggle({
                item,
                service: CONFIG.service,
                loadFn: loadSuppliersData,
                singularName: CONFIG.singularName
            })
        }
    });

    await initPage({
        ...CONFIG,
        extraActions: btnNew,
        onLoadData: loadSuppliersData
    });
}

// Carga los datos de los proveedores
async function loadSuppliersData() {
    await loadData({
        service: CONFIG.service,
        renderFn: (data) => supplierTable.setData(data)
    });
}

// Muestra el modal para crear o editar un proveedor
function handleShowSupplierModal(supplier = null) {
    showModal({
        ...CONFIG,
        item: supplier,
        onSubmit: async (e, form) => {
            await handleSubmit(e, {
                service: CONFIG.service,
                modalId: CONFIG.modalId,
                loadFn: loadSuppliersData,
                singularName: CONFIG.singularName
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', initSuppliersPage);
