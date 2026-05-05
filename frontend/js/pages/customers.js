// Lógica para la gestión de clientes

import { serviceProvider } from '../services/ServiceProvider.js';
import { initPage, loadData, handleToggle, showModal, handleSubmit, createNewButton } from '../utils/base_page.js';
import { formatDate, formatFullName } from '../utils/helpers.js';
import { Table } from '../components/Table.js';

const CONFIG = {
    pageName: 'Clientes',
    htmlFile: 'customers.html',
    service: serviceProvider.customers,
    singularName: 'cliente',
    modalId: 'modal-customer',
    formId: 'form-customer',
    template: 'customer',
    tableBodySelector: '.table tbody'
};

let customerTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `#${item.id}` },
    { label: 'Nombre', type: 'primary', value: (item) => item.first_name || '-' },
    { label: 'Apellido', type: 'primary', value: (item) => item.last_name || '-' },
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

// Inicializa la página de clientes
async function initCustomersPage() {
    const btnNew = createNewButton('btn-new-customer', 'Nuevo Cliente', () => handleShowCustomerModal());

    customerTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
        actions: {
            onEdit: handleShowCustomerModal,
            onToggle: (item) => handleToggle({
                item,
                service: CONFIG.service,
                loadFn: loadCustomersData,
                singularName: CONFIG.singularName
            })
        }
    });

    await initPage({
        ...CONFIG,
        extraActions: btnNew,
        onLoadData: loadCustomersData
    });
}

// Carga los datos de los clientes
async function loadCustomersData() {
    await loadData({
        service: CONFIG.service,
        renderFn: (data) => customerTable.setData(data)
    });
}

// Muestra el modal para crear o editar un cliente
function handleShowCustomerModal(customer = null) {
    showModal({
        ...CONFIG,
        item: customer,
        onSubmit: async (e, form) => {
            await handleSubmit(e, {
                service: CONFIG.service,
                modalId: CONFIG.modalId,
                loadFn: loadCustomersData,
                singularName: CONFIG.singularName
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', initCustomersPage);
