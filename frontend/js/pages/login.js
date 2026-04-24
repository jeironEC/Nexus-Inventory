/**
 * LOGIN.JS
 * El fetch/auth lo conectará el compañero de backend.
*/

document.addEventListener('DOMContentLoaded', function () {

    // TOGGLE CONTRASEÑA
    const passwordToggle = document.getElementById('password-toggle');
    const passwordInput  = document.getElementById('password');

    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener('click', function () {
            const isPassword = passwordInput.type === 'password';
            passwordInput.type = isPassword ? 'text' : 'password';

            const icon = passwordToggle.querySelector('.material-symbols-outlined');
            if (icon) {
                icon.textContent = isPassword ? 'visibility' : 'visibility_off';
            }
        });
    }

    // ESTADO DE CARGA DEL BOTÓN
    const form      = document.getElementById('login-form');
    const submitBtn = form ? form.querySelector('button[type="submit"]') : null;

    if (form && submitBtn) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            // Redirigir a index.html
            window.location.href = '../index.html';
        });
    }

});
