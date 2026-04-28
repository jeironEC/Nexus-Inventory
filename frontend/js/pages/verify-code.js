/**
 * VERIFY-CODE.JS
 * Al verificar el código:
 *  1. Muestra modal "Código verificado"
 *  2. Al aceptar, redirige a new-password.html
 */

document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('form-verify-code');
    if (!form) return;

    // Solo permitir números en el input OTP
    const otpInput = document.getElementById('otp-code');
    if (otpInput) {
        otpInput.addEventListener('input', function () {
            otpInput.value = otpInput.value.replace(/\D/g, '');
        });
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // El backend conectará aquí el POST
        // Cuando el backend responda OK, mostrar el modal:

        if (window.modal && typeof window.modal.showConfirm === 'function') {
            window.modal.showConfirm(
                'Código verificado',
                '¡Listo! Ahora puedes crear tu nueva contraseña.',
                function () {
                    window.location.href = 'new-password.html';
                }
            );
        } else {
            window.location.href = 'new-password.html';
        }
    });

});
