/**
 * COMPANY-SETUP.JS
 * Configuración inicial de empresa (estilo login).
 * Se muestra solo la primera vez para crear la empresa.
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {
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
