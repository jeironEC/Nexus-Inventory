// Lógica para la página de inicio de sesión

import { authService } from '../services/AuthService.js';
import * as helpers from '../utils/helpers.js';
window.helpers = helpers;

// Inicializa la página de login
function initLogin() {
    const form = document.getElementById('login-form');
    const passwordToggle = document.getElementById('password-toggle');

    // Redirigir si ya está autenticado
    if (authService.isAuthenticated()) {
        window.location.href = '/html/dashboard.html';
        return;
    }

    // Configurar toggle de contraseña
    if (passwordToggle) {
        passwordToggle.addEventListener('click', togglePasswordVisibility);
    }

    // Configurar envío de formulario
    if (form) {
        form.addEventListener('submit', handleLoginSubmit);
    }
}

// Alterna la visibilidad de la contraseña
function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    if (!passwordInput) return;

    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;

    const icon = this.querySelector('.material-symbols-outlined');
    if (icon) {
        icon.textContent = type === 'password' ? 'visibility_off' : 'visibility';
    }
}

// Maneja el envío del formulario de login
async function handleLoginSubmit(e) {
    e.preventDefault();
    const form = e.currentTarget;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const submitBtn = form.querySelector('button[type="submit"]');

    if (!submitBtn) return;

    const originalContent = helpers.setButtonLoading(submitBtn, true);

    try {
        const result = await authService.login(email, password);

        if (result.success) {
            try {
                // Obtener perfil para activar RBAC
                const { userService } = await import('../services/UserService.js');

                const profileRes = await userService.getUserProfile();

                // Determinar el rol de forma robusta
                let roleName = null;
                if (profileRes?.success && profileRes?.data) {
                    const profileData = profileRes.data;

                    // Extraer rol (puede venir como objeto o string)
                    const roleData = profileData.role;
                    if (typeof roleData === 'object' && roleData !== null) {
                        roleName = roleData.name;
                    } else if (typeof roleData === 'string') {
                        roleName = roleData;
                    }

                    const savedUser = {
                        id: profileData.id,
                        first_name: profileData.first_name,
                        last_name: profileData.last_name,
                        email: profileData.email,
                        role: roleName,
                    };

                    localStorage.setItem('auth_user', JSON.stringify(savedUser));

                    // Verificar si es administrador para check de empresas
                    if (roleName?.toLowerCase() === 'admin' || roleName?.toLowerCase() === 'administrador') {
                        const { serviceProvider } = await import('../services/ServiceProvider.js');
                        const companiesRes = await serviceProvider.companies.getAll({ limit: 1 });
                        const companies = companiesRes?.data?.results ?? companiesRes?.data ?? [];
                        const count = Array.isArray(companies) ? companies.length : 0;

                        if (count === 0) {
                            window.location.href = '/html/company_setup.html';
                            return;
                        }
                    }
                }
            } catch (err) {
            }

            window.location.href = '/html/dashboard.html';
        }
    } catch (error) {
        window.modal.showAlert('Atención', error.message || 'Error al iniciar sesión. Por favor, verifica tus credenciales.', 'error');

        // Restaurar estado del botón en caso de error
        helpers.setButtonLoading(submitBtn, false, originalContent);
    }
}

// Iniciar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initLogin);
