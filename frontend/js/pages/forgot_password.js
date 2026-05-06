// Lógica para la recuperación de contraseña

import { passwordResetService } from '../services/PasswordResetService.js';
import * as helpers from '../utils/helpers.js';

window.addEventListener('DOMContentLoaded', () => {
    const btnSubmit = document.getElementById('btn-submit');
    if (!btnSubmit) return;

    btnSubmit.addEventListener('click', async (e) => {
        e.preventDefault();

        const emailInput = document.getElementById('email');
        const email = emailInput.value.trim();

        if (!email) {
            emailInput.focus();
            return;
        }

        const originalContent = helpers.setButtonLoading(btnSubmit, true);

        try {
            await passwordResetService.requestRecovery(email);
            sessionStorage.setItem('reset_email', email);

            window.modal.showAlert(
                'Correo validado',
                'Correo verificado. Ahora puedes establecer tu nueva contraseña.',
                'success',
                () => { window.location.href = '/html/change_password.html'; }
            );
        } catch (error) {
            const message = error.data?.detail
                || error.data?.message
                || 'No pudimos procesar tu solicitud. Intenta de nuevo más tarde.';

            window.modal.showAlert('Error', message, 'error');
        } finally {
            helpers.setButtonLoading(btnSubmit, false, originalContent);
        }
    });
});
