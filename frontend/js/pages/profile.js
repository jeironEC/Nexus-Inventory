/**
 * PROFILE.JS
 * Inicializa los componentes de la página Mi Perfil:
 *  - Sidebar con la página activa marcada
 *  - Header con el título "Mi Perfil"
 *  - Toggle de contraseñas
 *  - Cambiar avatar (preview local — el upload real lo conecta el compañero)
 *  - Confirmación al eliminar cuenta
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

    // ─── Cambiar avatar ────────────────────────────────────────────
    const btnEditAvatar = document.getElementById('btn-edit-avatar');
    const inputAvatar   = document.getElementById('input-avatar');
    const avatarBox     = document.getElementById('profile-avatar');

    if (btnEditAvatar && inputAvatar) {
        btnEditAvatar.addEventListener('click', function () {
            inputAvatar.click();
        });

        inputAvatar.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (!file) return;

            // Preview local — en backend se hará el upload
            const reader = new FileReader();
            reader.onload = function (event) {
                // Vaciar el contenido sin innerHTML
                while (avatarBox.firstChild) {
                    avatarBox.removeChild(avatarBox.firstChild);
                }
                const img = document.createElement('img');
                img.src = event.target.result;
                img.alt = 'Avatar';
                avatarBox.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
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

    // ─── Eliminar cuenta ──────────────
    const btnDeleteAccount = document.getElementById('btn-delete-account');
    if (btnDeleteAccount) {
        btnDeleteAccount.addEventListener('click', function () {
            if (window.modal && typeof window.modal.showConfirm === 'function') {
                window.modal.showConfirm(
                    'Eliminar cuenta',
                    '¿Estás seguro de que quieres eliminar tu cuenta? Esta acción es permanente y no se puede deshacer.',
                    function () {
                        // El compañero conectará aquí el DELETE a /v1/users/me/
                        console.log('Cuenta eliminada (placeholder)');
                    }
                );
            }
        });
    }

});
