// Lógica para cambiar la contraseña

import { toast } from '../components/Toast.js';
import { passwordResetService } from '../services/PasswordResetService.js';
import { ValidationHelper } from '../utils/ValidationHelper.js';
import * as helpers from '../utils/helpers.js';

// Alterna la visibilidad de un campo de contraseña
function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon = btn.querySelector('.material-symbols-outlined');

    if (input.type === 'password') {
        input.type = 'text';
        icon.textContent = 'visibility';
    } else {
        input.type = 'password';
        icon.textContent = 'visibility_off';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const btnSubmit = document.getElementById('btn-submit');
    const newPasswordInput = document.getElementById('new_password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const requirementsContainer = document.getElementById('password-reqs');

    if (!btnSubmit || !newPasswordInput || !confirmPasswordInput) return;

    if (newPasswordInput && requirementsContainer) {
        ValidationHelper.setupPasswordValidation(newPasswordInput, requirementsContainer);
    }

    const checkMatch = () => {
        const pw = newPasswordInput.value;
        const cpw = confirmPasswordInput.value;

        if (!cpw) {
            confirmPasswordInput.style.borderColor = '';
            const hintEl = document.getElementById('confirm-hint');
            if (hintEl) hintEl.textContent = '';
            return;
        }

        if (pw === cpw) {
            confirmPasswordInput.style.borderColor = '#22c55e';
            const hintEl = document.getElementById('confirm-hint');
            if (hintEl) {
                hintEl.textContent = 'Las contraseñas coinciden';
                hintEl.style.color = '#22c55e';
            }
        } else {
            confirmPasswordInput.style.borderColor = '#ef4444';
            const hintEl = document.getElementById('confirm-hint');
            if (hintEl) {
                hintEl.textContent = 'Las contraseñas no coinciden';
                hintEl.style.color = '#ef4444';
            }
        }
    };

    confirmPasswordInput.addEventListener('input', checkMatch);
    newPasswordInput.addEventListener('input', checkMatch);

    document.querySelectorAll('.password-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const wrapper = btn.closest('.password-wrapper');
            const input = wrapper.querySelector('input');
            togglePassword(input.id, btn);
        });
    });

    const resetEmail = sessionStorage.getItem('reset_email');

    if (!resetEmail) {
        window.location.href = '/html/forgot_password.html';
        return;
    }

    btnSubmit.addEventListener('click', async (e) => {
        e.preventDefault();

        const newPassword = newPasswordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (!newPassword) {
            toast.show('Por favor ingresa tu nueva contraseña.', 'warning');
            return;
        }

        if (!confirmPassword) {
            toast.show('Por favor confirma tu nueva contraseña.', 'warning');
            return;
        }

        if (!ValidationHelper.isPasswordValid(newPassword)) {
            toast.show('La contraseña no cumple con todos los requisitos mínimos de seguridad.', 'warning');
            return;
        }

        if (newPassword !== confirmPassword) {
            toast.show('Las contraseñas ingresadas no son iguales. Verifica ambos campos.', 'warning');
            return;
        }

        const originalContent = helpers.setButtonLoading(btnSubmit, true);

        try {
            await passwordResetService.resetPassword(resetEmail, newPassword);

            sessionStorage.removeItem('reset_email');

            window.modal.showConfirm(
                '¡Contraseña actualizada!',
                'Tu contraseña ha sido cambiada exitosamente. Ahora puedes iniciar sesión con tu nueva contraseña.',
                () => { window.location.href = '/index.html'; }
            );
        } catch (error) {
            const message = error.data?.detail
                || error.data?.message
                || error.data?.non_field_errors?.[0]
                || (error.data?.new_password
                    ? (Array.isArray(error.data.new_password) ? error.data.new_password.join(', ') : error.data.new_password)
                    : 'No pudimos cambiar tu contraseña. Intenta de nuevo más tarde.');

            window.modal.showAlert('Error', message, 'error');
        } finally {
            helpers.setButtonLoading(btnSubmit, false, originalContent);
        }
    });
});
