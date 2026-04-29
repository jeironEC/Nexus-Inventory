/**
 * PROFILE.JS
 * Inicializa los componentes de la página Mi Perfil:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Mi Perfil"
 *  - Toggle de contraseñas
 *
 * SIN fetch ni conexiones a API.
 */

document.addEventListener('DOMContentLoaded', function () {

    if (window.sidebar) {
        window.sidebar.init('profile.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Mi Perfil');
    }

    // ─── Toggle de contraseñas ──
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(function (toggle) {
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

    // ─── Submit: información personal ──────────────────────────────
    const formProfileInfo = document.getElementById('form-profile-info');
    if (formProfileInfo) {
        formProfileInfo.addEventListener('submit', function (e) {
            e.preventDefault();
            // El compañero conectará aquí el PATCH a /v1/users/me/
            console.log('Formulario información personal enviado');
        });
    }

    // ─── Submit: cambiar contraseña ────────────────────────────────
    const formChangePassword = document.getElementById('form-change-password');
    if (formChangePassword) {
        formChangePassword.addEventListener('submit', function (e) {
            e.preventDefault();
            // El compañero conectará aquí el POST de password-reset
            console.log('Formulario cambiar contraseña enviado');
        });
    }
});
