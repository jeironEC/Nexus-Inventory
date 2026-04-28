/**
 * COMPANY.JS
 * Inicializa la página de Perfil Empresa:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Perfil Empresa"
 *  - Cambiar logo (preview local)
 *  - Submit del formulario
 *  - Confirmación al eliminar empresa
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('company.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Perfil Empresa');
    }

    // ─── Cambiar logo ──────────────────────────────────────────────
    const btnEditLogo = document.getElementById('btn-edit-logo');
    const inputLogo   = document.getElementById('input-logo');
    const logoBox     = document.getElementById('company-logo-header');

    if (btnEditLogo && inputLogo) {
        btnEditLogo.addEventListener('click', function () {
            inputLogo.click();
        });

        inputLogo.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function (event) {
                while (logoBox.firstChild) {
                    logoBox.removeChild(logoBox.firstChild);
                }
                const img = document.createElement('img');
                img.src = event.target.result;
                img.alt = 'Logo de la empresa';
                logoBox.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    }

    // ─── Submit: información de la empresa ─────────────────────────
    const form = document.getElementById('form-company-info');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            // El cbackend conectará aquí el PATCH
            console.log('Formulario empresa enviado');
        });
    }
});
