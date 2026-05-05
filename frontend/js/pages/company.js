// Lógica para mostrar y editar los datos de la empresa

import '../components/Modal.js';
import '../components/Sidebar.js';
import '../components/PageHeader.js';
import { serviceProvider } from '../services/ServiceProvider.js';
import { authService } from '../services/AuthService.js';
import { toast } from '../components/Toast.js';
import { setButtonLoading } from '../utils/helpers.js';

// Inicializa la página de empresa
async function initCompanyPage() {
    if (!authService.isAuthenticated()) {
        window.location.href = '/index.html';
        return;
    }

    if (window.sidebar) {
        window.sidebar.init('company.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Empresa', { showSearch: false });
    }

    await loadCompanyData();
}

// Carga los datos de la empresa desde el servidor
async function loadCompanyData() {
    try {
        const response = await serviceProvider.companies.getAll({ limit: 1 });

        if (response.success && response.data) {
            const companies = response.data.results || response.data;
            if (companies && companies.length > 0) {
                window.currentCompanyId = companies[0].id;
                populateCompanyForm(companies[0]);
            } else {
                toast.show('No se encontró información de la empresa. Contacta al administrador.', 'warning');
            }
        } else {
            toast.show('No se pudieron cargar los datos de la empresa.', 'error');
        }
    } catch (error) {
        toast.show(`Error al comunicar con el servidor: ${error.message}`, 'error');
    }
}

// Rellena el formulario con los datos de la empresa
function populateCompanyForm(companyData) {
    const logoHeader = document.getElementById('company-logo-header');
    if (companyData.logo) {
        logoHeader.innerHTML = `<img src="${companyData.logo}" alt="Logo" onerror="this.style.display='none'; this.parentElement.querySelector('.logo-fallback').style.display='flex';">`;
        const fallback = document.createElement('div');
        fallback.className = 'logo-fallback';
        fallback.style.cssText = 'display:none;align-items:center;justify-content:center;width:100%;height:100%;';
        const initials = (companyData.name || 'Empresa').split(' ').filter(Boolean).map(w => w.charAt(0).toUpperCase()).join('');
        fallback.textContent = initials;
        logoHeader.appendChild(fallback);
    } else {
        const initials = (companyData.name || 'Empresa').split(' ').filter(Boolean).map(w => w.charAt(0).toUpperCase()).join('');
        logoHeader.innerHTML = `<span class="logo-letter" style="font-family:var(--font-display);font-size:48px;font-weight:700;color:var(--white);">${initials}</span>`;
    }

    document.getElementById('company-display-name').textContent = companyData.name || 'Nombre de la Empresa';
    document.getElementById('company-display-nif').textContent = companyData.nif ? `NIF: ${companyData.nif}` : 'NIF: ---';

    const stateBadge = document.getElementById('company-state');
    const isActive = companyData.is_active !== false;
    stateBadge.textContent = isActive ? 'Activa' : 'Inactiva';
    stateBadge.className = `badge ${isActive ? 'badge-success' : 'badge-danger'}`;

    document.getElementById('company-name').value = companyData.name || '';
    document.getElementById('company-nif').value = companyData.nif || '';
    document.getElementById('company-email').value = companyData.email || '';
    document.getElementById('company-phone').value = companyData.number_phone || '';
    document.getElementById('company-website').value = companyData.website || '';
    document.getElementById('company-address').value = companyData.address || '';

    setupLogoUpload(companyData.name);

    document.getElementById('form-company-info').addEventListener('submit', handleCompanyUpdate);
}

// Configura la subida y previsualización del logo
function setupLogoUpload(companyName) {
    const editBtn = document.getElementById('company-logo-edit');
    const logoInput = document.getElementById('logo-input');
    const logoHeader = document.getElementById('company-logo-header');

    if (editBtn && logoInput) {
        editBtn.addEventListener('click', () => logoInput.click());
    }

    if (logoInput && logoHeader) {
        logoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    logoHeader.innerHTML = `<img src="${e.target.result}" alt="Logo Preview">`;
                };
                reader.readAsDataURL(file);
            }
        });
    }
}

// Maneja el envío del formulario de actualización de empresa
async function handleCompanyUpdate(e) {
    e.preventDefault();
    const btn = document.getElementById('btn-save-company');
    const originalContent = setButtonLoading(btn, true);

    const form = e.target;
    const formData = new FormData();

    formData.append('nif', form.nif.value.trim());
    formData.append('name', form.name.value.trim());
    formData.append('address', form.address.value.trim());
    formData.append('number_phone', form.number_phone.value.trim());
    formData.append('email', form.email.value.trim());

    if (form.website.value.trim()) {
        formData.append('website', form.website.value.trim());
    }

    const logoFile = document.getElementById('logo-input').files[0];
    if (logoFile) {
        formData.append('logo', logoFile);
    }

    try {
        const response = await serviceProvider.companies.update(window.currentCompanyId, formData);

        if (response.success) {
            toast.show('Datos de la empresa actualizados correctamente.', 'success');
            await loadCompanyData();
        } else {
            toast.show(response.message || 'No se pudieron actualizar los datos.', 'error');
        }
    } catch (error) {
        toast.show(error.message || 'Fallo de conexión.', 'error');
    } finally {
        setButtonLoading(btn, false, originalContent);
    }
}

document.addEventListener('DOMContentLoaded', initCompanyPage);
