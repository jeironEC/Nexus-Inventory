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
            const result = await passwordResetService.requestRecovery(email);
            sessionStorage.setItem('reset_email', email);

            let displayMessage = result.message;
            if (displayMessage.includes('If the email address exists')) {
                displayMessage = 'Si el correo está registrado, recibirás un código de verificación en tu bandeja de entrada.';
            }

            window.modal.showAlert(
                'Correo enviado',
                displayMessage,
                'success',
                () => { window.location.href = '/html/verify_otp.html'; }
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
