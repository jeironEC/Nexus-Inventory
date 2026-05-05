// Lógica para la gestión de usuarios

import { toast } from '../components/Toast.js';
import { serviceProvider } from '../services/ServiceProvider.js';
import { authService } from '../services/AuthService.js';
import { initPage, loadData, showModal, handleSubmit, createNewButton } from '../utils/base_page.js';
import { ValidationHelper } from '../utils/ValidationHelper.js';
import { getInitials, formatFullName, formatDate } from '../utils/helpers.js';
import { Table } from '../components/Table.js';

const CONFIG = {
    pageName: 'Usuarios',
    htmlFile: 'users.html',
    service: serviceProvider.users,
    singularName: 'usuario',
    modalId: 'modal-user',
    formId: 'form-user',
    template: 'user',
    tableBodySelector: '.table tbody',
    filterSelectIds: ['user-filter-role-id']
};

let userTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `#${item.id}` },
    {
        label: 'Avatar',
        type: 'primary',
        value: (item) => {
            const initials = getInitials(item);
            const content = initials ? initials : `<span class="material-symbols-outlined" style="font-size: 18px;">person</span>`;
            return `<div style="width: 32px; height: 32px; border-radius: 50%; background: var(--royal); color: white; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold;">${content}</div>`;
        }
    },
    { label: 'Nombre', type: 'primary', value: (item) => item.first_name || '-' },
    { label: 'Apellido', type: 'primary', value: (item) => item.last_name || '-' },
    { label: 'Email', type: 'normal', value: (item) => item.email || '-' },
    { label: 'NIF', type: 'normal', value: (item) => item.nif || '-' },
    { label: 'Rol', type: 'normal', value: (item) => item.role?.name || '-' },
    { label: 'Estado', type: 'normal', value: (item) => `<span class="badge ${item.is_active ? 'badge-success' : 'badge-danger'}">${item.is_active ? 'Activo' : 'Inactivo'}</span>` },
    { label: 'Creado en', type: 'normal', value: (item) => item.created_at ? formatDate(item.created_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Actualizado en', type: 'normal', value: (item) => item.updated_at ? formatDate(item.updated_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Eliminado en', type: 'normal', value: (item) => item.deleted_at ? formatDate(item.deleted_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Creado por', type: 'audit', value: (item) => item.created_by?.first_name ? formatFullName(item.created_by) : (item.created_by?.email || '-') },
    { label: 'Actualizado por', type: 'audit', value: (item) => item.updated_by?.first_name ? formatFullName(item.updated_by) : (item.updated_by?.email || '-') },
    { label: 'Eliminado por', type: 'audit', value: (item) => item.deleted_by?.first_name ? formatFullName(item.deleted_by) : (item.deleted_by?.email || '-') }
];

// Inicializa la página de usuarios
async function initUsersPage() {
    const btnNew = createNewButton('btn-new-user', 'Nuevo Usuario', () => handleShowUserModal());

    userTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
        actions: {
            onEdit: handleShowUserModal,
            onToggle: handleUserToggle
        }
    });

    await initPage({
        ...CONFIG,
        extraActions: btnNew,
        onLoadData: loadUsersData
    });
}

// Maneja activación/desactivación de usuario con lógica especial para el usuario actual
async function handleUserToggle(item) {
    const isActive = item.is_active;
    const action = isActive ? 'desactivar' : 'activar';
    const name = item.first_name || item.email || `#${item.id}`;
    window.modal.showConfirm(
        'Confirmar acción',
        `¿Estás seguro de que deseas ${action} al usuario "${name}"?`,
        async () => {
            try {
                const response = isActive
                    ? await CONFIG.service.deactivate(item.id)
                    : await CONFIG.service.activate(item.id);

                if (response.success) {
                    const isSelf = isActive && item.id === JSON.parse(localStorage.getItem('auth_user') || '{}').id;

                    if (isSelf) {
                        window.modal.showAlert(
                            'Sesión cerrada',
                            'Tu cuenta ha sido desactivada. Tu sesión será cerrada.',
                            'warning'
                        );
                        const okBtn = document.getElementById('modal-dynamic-alert-ok');
                        if (okBtn) {
                            okBtn.onclick = () => {
                                authService.logout();
                                window.location.href = '/index.html';
                            };
                        }
                        return;
                    }

                    toast.show(`Usuario ${action === 'activar' ? 'activado' : 'desactivado'} correctamente`, 'success');
                    await loadUsersData();
                } else {
                    window.modal.showAlert('Error', response.message || `No se pudo ${action} el usuario`, 'error');
                }
            } catch (error) {
                window.modal.showAlert('Error', error.message || `Error al ${action} el usuario`, 'error');
            }
        }
    );
}

// Carga los datos de los usuarios
async function loadUsersData() {
    await loadData({
        service: CONFIG.service,
        renderFn: (data) => userTable.setData(data)
    });
}

// Muestra el modal para crear o editar un usuario
async function handleShowUserModal(user = null) {
    await showModal({
        ...CONFIG,
        item: user,
        onShow: async (form, item) => {
            try {
                const rolesRes = await serviceProvider.roles.getAll({ limit: 100 });
                if (rolesRes.success && rolesRes.data) {
                    const roles = rolesRes.data.results || rolesRes.data;
                    const select = form.querySelector('select[name="role"]');
                    const { populateSelect } = await import('../utils/form_utils.js');
                    const selectedVal = (item && item.role) ? item.role.id : null;
                    populateSelect(select, roles, 'name', 'id', selectedVal);
                }
            } catch(e) {}

            const passInput = form.querySelector('input[name="password"]');
            const reqDiv = form.querySelector('.password-requirements');

            if (passInput && reqDiv) {
                ValidationHelper.setupPasswordValidation(passInput, reqDiv);
            }

            if (item) {
                if (passInput) {
                    passInput.required = false;
                    passInput.placeholder = "Dejar en blanco para no cambiar";
                }
                if (reqDiv) reqDiv.style.display = 'none';
            }
        },
        onSubmit: async (e, form) => {
            const passwordVal = form['password'] ? form['password'].value.trim() : '';
            const roleVal = form['role'] ? form['role'].value : null;

            if (!user || passwordVal) {
                if (!ValidationHelper.isPasswordValid(passwordVal)) {
                    if (window.modal) {
                        toast.show('La contraseña no cumple con los requisitos mínimos de seguridad.', 'warning');
                    }
                    return;
                }
            }

            const formData = new FormData();
            formData.append('first_name', form['first_name']?.value.trim() || '');
            formData.append('last_name', form['last_name']?.value.trim() || '');
            formData.append('email', form['email']?.value.trim() || '');
            formData.append('nif', form['nif']?.value.trim() || '');
            if (roleVal) formData.append('role', roleVal);

            if (passwordVal) formData.append('password', passwordVal);

            await handleSubmit(e, {
                service: CONFIG.service,
                modalId: CONFIG.modalId,
                loadFn: loadUsersData,
                singularName: CONFIG.singularName,
                customData: formData
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', initUsersPage);
