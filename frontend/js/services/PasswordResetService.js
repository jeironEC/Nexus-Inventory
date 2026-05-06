// Gestiona el flujo de recuperación de contraseña

import { ApiClient } from "../api/ApiClient.js";
import {
    URL_BASE,
    URL_PASSWORD_RESET_REQUEST,
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

    // Verifica email de admin y permite cambio de contraseña
    async requestRecovery(email) {
        try {
            const response = await this.api.post(
                URL_PASSWORD_RESET_REQUEST,
                { email },
                this.getSesionOptions()
            );

            return {
                success: true,
                message: response.data?.detail || response.data?.message || 'Correo verificado. Puedes cambiar tu contraseña.'
            };
        } catch (error) {
            throw error;
        }
    }

    // Restablece la contraseña
    async resetPassword(email, newPassword) {
        try {
            const response = await this.api.post(
                URL_PASSWORD_RESET_CONFIRM,
                { email: email, new_password: newPassword },
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
