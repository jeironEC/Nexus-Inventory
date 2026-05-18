// Controlador para el registro inicial de la empresa

import { serviceProvider } from '../services/ServiceProvider.js';
import { authService } from '../services/AuthService.js';
import { setButtonLoading } from '../utils/helpers.js';
import { ValidationHelper } from '../utils/ValidationHelper.js';

// Inicializa la configuración inicial de la empresa
async function initCompanySetup() {
    if (!authService.isAuthenticated()) {
        window.location.replace('/index.html');
        return;
    }

    const form = document.getElementById('company-setup-form');
    if (form) {
        form.addEventListener('submit', handleCompanySetupSubmit);
    }
}

// Maneja el envío del formulario de registro de empresa
async function handleCompanySetupSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const btn = document.getElementById('btn-company-submit');

    if (!ValidationHelper.validateForm(form)) {
        return;
    }

    const originalNodes = setButtonLoading(btn, true);

    const payload = {
        nif: form.nif.value.trim(),
        name: form.name.value.trim(),
        address: form.address.value.trim(),
        number_phone: form.number_phone.value.trim(),
        email: form.email.value.trim(),
        website: form.website.value.trim() || null,
        logo: form.logo.value.trim() || null
    };

    try {
        const response = await serviceProvider.companies.create(payload);

        if (response.success) {
            window.isNavigatingAway = true;
            window.location.href = '/html/dashboard.html';
        }
    } catch (error) {
        if (window.modal && typeof window.modal.showAlert === 'function') {
            window.modal.showAlert('Error', error.message || 'Error de conexión al registrar la empresa.', 'error');
        } else {
            alert(`Error: ${error.message || 'Error de conexión al registrar la empresa.'}`);
        }
    } finally {
        setButtonLoading(btn, false, originalNodes);
    }
}

// Protege la navegación: si el usuario intenta salir sin completar, limpia la sesión
function setupNavigationGuard() {
    window.addEventListener('popstate', function(e) {
        if (window.isNavigatingAway) return;
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('auth_user');
        window.location.href = '/index.html';
    });

    window.addEventListener('beforeunload', function(e) {
        if (window.isNavigatingAway) return;
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('auth_user');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    setupNavigationGuard();
    initCompanySetup();
});
