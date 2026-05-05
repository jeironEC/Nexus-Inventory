// Gestiona el flujo de recuperación de contraseña

import { ApiClient } from "../api/ApiClient.js";
import {
    URL_BASE,
    URL_PASSWORD_RESET_REQUEST,
    URL_PASSWORD_RESET_VERIFY,
    URL_PASSWORD_RESET_CONFIRM,
    DEFAULT_TIMEOUT,
    CSRFTOKEN_KEY
} from "../utils/const.js";

class PasswordResetService {
    constructor() {
        this.api = new ApiClient(URL_BASE, {
            timeout: DEFAULT_TIMEOUT
        });
    }

    getCsrfToken() {
        if (!document.cookie) return null;

        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === CSRFTOKEN_KEY) {
                return decodeURIComponent(value);
            }
        }
        return null;
    }

    getSesionOptions() {
        const csrfToken = this.getCsrfToken();
        return csrfToken ? { headers: { 'X-CSRFTOKEN': csrfToken } } : {};
    }

    // Solicita código OTP para recuperación
    async requestRecovery(email) {
        try {
            const response = await this.api.post(
                URL_PASSWORD_RESET_REQUEST,
                { email },
                this.getSesionOptions()
            );

            return {
                success: true,
                message: response.data?.detail || response.data?.message || 'Se ha enviado un código de verificación a tu correo.'
            };
        } catch (error) {
            throw error;
        }
    }

    // Verifica el código OTP
    async verifyRecoveryOtp(email, otp) {
        try {
            const response = await this.api.post(
                URL_PASSWORD_RESET_VERIFY,
                { email, otp },
                this.getSesionOptions()
            );

            return {
                success: true,
                reset_token: response.data?.reset_token,
                message: response.data?.message || 'Código verificado correctamente.'
            };
        } catch (error) {
            throw error;
        }
    }

    // Restablece la contraseña
    async resetPassword(resetToken, newPassword) {
        try {
            const response = await this.api.post(
                URL_PASSWORD_RESET_CONFIRM,
                { reset_token: resetToken, new_password: newPassword },
                this.getSesionOptions()
            );

            return {
                success: true,
                message: response.data?.detail || response.data?.message || 'Tu contraseña ha sido actualizada correctamente.'
            };
        } catch (error) {
            throw error;
        }
    }
}

export const passwordResetService = new PasswordResetService();
