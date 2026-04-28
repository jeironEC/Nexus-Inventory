/**
 * FORGOT-PASSWORD.JS (actualizado)
 * Al enviar el formulario:
 *  1. Muestra modal "Correo enviado"
 *  2. Al aceptar, redirige a verify-code.html
 *
 */

document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('forgot-password-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // El backend conectará aquí el POST
        // Cuando el backend responda OK, mostrar el modal:

        if (window.modal && typeof window.modal.showConfirm === 'function') {
            window.modal.showConfirm(
                'Correo enviado',
                'Si el correo está registrado, recibirás un código de verificación.',
                function () {
                    // Al aceptar  ir a verificar código
                    window.location.href = 'verify-code.html';
                }
            );
        } else {
            // Fallback si el modal no está cargado
            window.location.href = 'verify-code.html';
        }
    });

});
