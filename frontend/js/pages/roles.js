// Lógica para la gestión de roles

import { serviceProvider } from '../services/ServiceProvider.js';
import { initPage, loadData, handleToggle, showModal, handleSubmit, createNewButton } from '../utils/base_page.js';
import { formatDate } from '../utils/helpers.js';
import { Table } from '../components/Table.js';

const CONFIG = {
    pageName: 'Roles',
    htmlFile: 'roles.html',
    service: serviceProvider.roles,
    singularName: 'rol',
    modalId: 'modal-role',
    formId: 'form-role',
    template: 'role',
    tableBodySelector: '.table tbody'
};

const ROLE_OPTIONS = {
    'admin': 'rol de administración',
    'cajero': 'rol de cajero',
    'encargado de ventas': 'rol de encargado de ventas',
    'encargado de compras': 'rol de encargado de compras'
};

let roleTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `#${item.id}` },
    { label: 'Nombre', type: 'primary', value: (item) => item.name ? item.name.charAt(0).toUpperCase() + item.name.slice(1).toLowerCase() : '' },
    { label: 'Descripción', type: 'normal', value: (item) => item.description || '-' },
    { label: 'Estado', type: 'normal', value: (item) => `<span class="badge ${item.is_active ? 'badge-success' : 'badge-danger'}">${item.is_active ? 'Activo' : 'Inactivo'}</span>` },
    { label: 'Creado en', type: 'normal', value: (item) => item.created_at ? formatDate(item.created_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Actualizado en', type: 'normal', value: (item) => item.updated_at ? formatDate(item.updated_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Eliminado en', type: 'normal', value: (item) => item.deleted_at ? formatDate(item.deleted_at, 'dd/mm/yyyy HH:mm') : '-' }
];

// Inicializa la página de roles
async function initRolesPage() {
    const btnNew = createNewButton('btn-new-role', 'Nuevo Rol', () => handleShowRoleModal());

    roleTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
        actions: {
            onToggle: (item) => handleToggle({
                item,
                service: CONFIG.service,
                loadFn: loadRolesData,
                singularName: CONFIG.singularName
            })
        }
    });

    await initPage({
        ...CONFIG,
        extraActions: btnNew,
        onLoadData: loadRolesData
    });
}

// Carga los datos de los roles
async function loadRolesData() {
    await loadData({
        service: CONFIG.service,
        renderFn: (data) => roleTable.setData(data)
    });
}

// Muestra el modal para crear un rol
async function handleShowRoleModal(role = null) {
    const existingNames = [];
    try {
        const res = await CONFIG.service.getAll({ limit: 100 });
        if (res.success && res.data) {
            const items = res.data.results || (Array.isArray(res.data) ? res.data : []);
            items.forEach(r => r.name && existingNames.push(r.name.toLowerCase()));
        }
    } catch (e) {}

    showModal({
        ...CONFIG,
        item: role,
        onShow: (form) => {
            const select = form.querySelector('#role-name-select');
            const descInput = form.querySelector('#role-description-input');

            if (!select || !descInput) return;

            select.innerHTML = '<option value="">Selecciona un rol</option>';
            Object.entries(ROLE_OPTIONS).forEach(([value, desc]) => {
                if (!existingNames.includes(value.toLowerCase())) {
                    const opt = document.createElement('option');
                    opt.value = value;
                    opt.textContent = value.charAt(0).toUpperCase() + value.slice(1);
                    select.appendChild(opt);
                }
            });

            select.addEventListener('change', () => {
                descInput.value = ROLE_OPTIONS[select.value] || '';
            });
        },
        onSubmit: async (e, form) => {
            await handleSubmit(e, {
                service: CONFIG.service,
                modalId: CONFIG.modalId,
                loadFn: loadRolesData,
                singularName: CONFIG.singularName
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', initRolesPage);
