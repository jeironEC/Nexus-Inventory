/**
 * NEW-PASSWORD.JS
 * Página de cambiar contraseña tras OTP.
 *
 *  1. Toggle de visibilidad para los dos inputs
 *  2. Validación visual en tiempo real de los 5 requisitos
 *  3. Al enviar: muestra modal "Contraseña actualizada" redirige a login
 *
 */

document.addEventListener('DOMContentLoaded', function () {

    const newPasswordInput     = document.getElementById('new-password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const form                 = document.getElementById('form-new-password');

    // ─── Toggle de visibilidad ─────────────────────────────────────
    const toggles = document.querySelectorAll('.password-toggle');
    toggles.forEach(function (toggle) {
        toggle.addEventListener('click', function () {
            const targetId = toggle.getAttribute('data-target');
            const input    = document.getElementById(targetId);
            if (!input) return;

            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';

            const icon = toggle.querySelector('.material-symbols-outlined');
            if (icon) {
                icon.textContent = isPassword ? 'visibility' : 'visibility_off';
            }
        });
    });

    // ─── Validación visual de requisitos en tiempo real ───────────
    if (newPasswordInput) {
        newPasswordInput.addEventListener('input', function () {
            const value = newPasswordInput.value;

            const checks = {
                length:    value.length >= 8,
                uppercase: /[A-Z]/.test(value),
                lowercase: /[a-z]/.test(value),
                number:    /\d/.test(value),
                special:   /[!@#$%^&*(),.?":{}|<>_\-+=/\\\[\];'`~]/.test(value)
            };

            Object.keys(checks).forEach(function (key) {
                const reqEl = document.querySelector('.password-req[data-req="' + key + '"]');
                if (!reqEl) return;

                const icon = reqEl.querySelector('.material-symbols-outlined');
                if (checks[key]) {
                    reqEl.classList.add('valid');
                    if (icon) icon.textContent = 'check';
                } else {
                    reqEl.classList.remove('valid');
                    if (icon) icon.textContent = 'close';
                }
            });
        });
    }

    // ─── Submit del formulario ────────────────────────────────────
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            // El backend conectará aquí el POST
            // Cuando el backend responda OK, mostrar el modal:

            if (window.modal && typeof window.modal.showConfirm === 'function') {
                window.modal.showConfirm(
                    '¡Contraseña actualizada!',
                    'Tu contraseña ha sido cambiada exitosamente. Ahora puedes iniciar sesión con tu nueva contraseña.',
                    function () {
                        window.location.href = 'login.html';
                    }
                );
            } else {
                window.location.href = 'login.html';
            }
        });
    }

});
