/**
 * COMPANY-SETUP.JS
 * Configuración inicial de empresa (estilo login).
 * Se muestra solo la primera vez para crear la empresa.
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Subir logo ────────────────────────────────────────────────
    const btnUploadLogo = document.getElementById('btn-upload-logo');
    const inputLogo     = document.getElementById('input-logo');
    const logoPreview   = document.getElementById('company-logo-preview');

    if (btnUploadLogo && inputLogo && logoPreview) {
        btnUploadLogo.addEventListener('click', function () {
            inputLogo.click();
        });

        inputLogo.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function (event) {
                // Vaciar el contenido sin innerHTML
                while (logoPreview.firstChild) {
                    logoPreview.removeChild(logoPreview.firstChild);
                }
                const img = document.createElement('img');
                img.src = event.target.result;
                img.alt = 'Logo';
                logoPreview.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    }

    // ─── Submit del formulario ─────────────────────────────────────
    const form = document.getElementById('form-company-setup');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            // El backend conectará aquí el POST
            console.log('Formulario configurar empresa enviado');
        });
    }

});
