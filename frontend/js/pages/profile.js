// Lógica para visualizar y editar el perfil del usuario

import { authService } from '../services/AuthService.js';
import { toast } from '../components/Toast.js';
import { userService } from '../services/UserService.js';
import { getInitials, formatFullName, setButtonLoading } from '../utils/helpers.js';
import { parseHTML } from '../utils/dom.js';
import { serviceProvider } from '../services/ServiceProvider.js';

// Inicializa la página de perfil
async function initProfilePage() {
    if (!authService.isAuthenticated()) {
        window.location.href = '/index.html';
        return;
    }

    if (window.sidebar) {
        window.sidebar.init('profile.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Mi Perfil');
    }

    await Promise.all([loadUserProfile(), loadRoles()]);
    document.getElementById('form-profile-info')?.addEventListener('submit', handleProfileUpdate);
}

// Carga los roles disponibles en el select
async function loadRoles() {
    try {
        const response = await serviceProvider.roles.getAll({ is_active: true });
        const select = document.getElementById('profile-role-select');
        if (!select) return;

        select.innerHTML = '';
        if (response.success && response.data) {
            const roles = response.data.results || response.data.data || response.data;
            if (Array.isArray(roles)) {
                roles.forEach(role => {
                    const opt = document.createElement('option');
                    opt.value = role.id;
                    opt.textContent = role.name;
                    select.appendChild(opt);
                });
            }
        }

        if (typeof Choices !== 'undefined' && !select.dataset.choicesInitialized) {
            try {
                const choices = new Choices(select, {
                    searchEnabled: true,
                    itemSelectText: '',
                    noResultsText: 'Sin resultados',
                    noChoicesText: 'Sin opciones',
                    shouldSort: false,
                    searchPlaceholderValue: 'Buscar...',
                });
                select._choices = choices;
                select.dataset.choicesInitialized = 'true';
            } catch (e) {
            }
        }
    } catch (error) {
        const select = document.getElementById('profile-role-select');
        if (select) {
            select.innerHTML = '<option value="">Error al cargar roles</option>';
        }
    }
}

// Carga los datos del perfil del usuario
async function loadUserProfile() {
    try {
        const response = await userService.getUserProfile();

        if (response.success && response.data) {
            populateProfile(response.data);

            const currAuth = JSON.parse(localStorage.getItem('auth_user') || '{}');
            currAuth.email = response.data.email || currAuth.email;
            currAuth.first_name = response.data.first_name;
            currAuth.last_name = response.data.last_name;
            localStorage.setItem('auth_user', JSON.stringify(currAuth));
        } else {
            toast.show('No se pudo cargar la información del perfil.', 'error');
        }
    } catch (error) {
        toast.show(`Error al comunicar con el servidor: ${error.message}`, 'error');
    }
}

// Rellena el formulario con los datos del perfil
function populateProfile(userData) {
    const initials = getInitials(userData);
    const fullName = formatFullName(userData);
    const roleName = userData.role?.name || (typeof userData.role === 'string' ? userData.role : 'Usuario');
    const roleId = userData.role?.id || (typeof userData.role === 'object' ? userData.role.id : null);

    const avatarContainer = document.getElementById('profile-avatar');
    const avatarEl = document.getElementById('profile-avatar-initials');

    if (initials) {
        avatarEl.textContent = initials;
        avatarEl.style.display = '';
    } else {
        avatarEl.style.display = 'none';
        if (avatarContainer && !avatarContainer.querySelector('.material-symbols-outlined')) {
            avatarContainer.appendChild(parseHTML('<span class="material-symbols-outlined" style="font-size: 48px;">person</span>'));
        }
    }

    document.getElementById('profile-name').textContent = fullName;
    document.getElementById('profile-email').textContent = userData.email;
    document.getElementById('profile-role').textContent = roleName;

    document.getElementById('profile-first-name').value = userData.first_name || '';
    document.getElementById('profile-last-name').value = userData.last_name || '';
    document.getElementById('profile-email-input').value = userData.email || '';
    document.getElementById('profile-nif').value = userData.nif || '';

    if (roleId) {
        document.getElementById('profile-role-select').value = roleId;
    }

    const form = document.getElementById('form-profile-info');
    form?.addEventListener('submit', handleProfileUpdate);
}

// Maneja el envío del formulario de actualización de perfil
async function handleProfileUpdate(e) {
    e.preventDefault();
    const btn = document.getElementById('btn-save-profile');
    const originalContent = setButtonLoading(btn, true);

    const form = e.target;
    const formData = new FormData();

    if (form.first_name.value.trim()) formData.append('first_name', form.first_name.value.trim());
    if (form.last_name.value.trim()) formData.append('last_name', form.last_name.value.trim());
    if (form.email.value.trim()) formData.append('email', form.email.value.trim());
    if (form.nif.value.trim()) formData.append('nif', form.nif.value.trim());
    if (form.role.value) formData.append('role', form.role.value);

    try {
        const response = await userService.updateUserProfile(formData);
        if (response.success) {
            toast.show('Perfil actualizado correctamente.', 'success');
            await loadUserProfile();

            if (window.pageHeader) {
                window.pageHeader.init('Mi Perfil');
            }
        } else {
            toast.show(response.message || 'No se pudo actualizar el perfil.', 'error');
        }
    } catch (error) {
        toast.show(error.message || 'Fallo de conexión al actualizar el perfil.', 'error');
    } finally {
        setButtonLoading(btn, false, originalContent);
    }
}

document.addEventListener('DOMContentLoaded', initProfilePage);
