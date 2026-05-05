// Lógica para verificar el código OTP

import { passwordResetService } from '../services/PasswordResetService.js';
import * as helpers from '../utils/helpers.js';

document.addEventListener('DOMContentLoaded', () => {
    const btnSubmit = document.getElementById('btn-submit');
    const otpInput = document.getElementById('otp');
    if (!btnSubmit || !otpInput) return;

    const savedEmail = sessionStorage.getItem('reset_email');
    if (!savedEmail) {
        window.location.href = '/html/forgot_password.html';
        return;
    }

    btnSubmit.addEventListener('click', async (e) => {
        e.preventDefault();

        const otp = otpInput.value.trim();

        if (!otp) {
            otpInput.focus();
            return;
        }

        if (otp.length !== 6) {
            window.modal.showAlert('Error', 'El código debe tener 6 dígitos.', 'warning');
            return;
        }

        const originalContent = helpers.setButtonLoading(btnSubmit, true);

        try {
            const result = await passwordResetService.verifyRecoveryOtp(savedEmail, otp);
            sessionStorage.setItem('reset_verified', 'true');
            sessionStorage.setItem('reset_token', result.reset_token);
            window.modal.showConfirm(
                'Código verificado',
                '¡Listo! Ahora puedes crear tu nueva contraseña.',
                () => { window.location.href = '/html/change_password.html'; }
            );
        } catch (error) {
            const message = error.data?.detail
                || error.data?.error
                || 'El código ingresado no es válido o ha expirado.';

            window.modal.showAlert('Error', message, 'error');
        } finally {
            helpers.setButtonLoading(btnSubmit, false, originalContent);
        }
    });
});
