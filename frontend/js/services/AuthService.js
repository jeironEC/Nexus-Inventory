// Gestiona la autenticación, tokens y estado del usuario

import { ApiClient } from "../api/ApiClient.js";
import {
    URL_BASE,
    URL_AUTH_TOKEN,
    URL_AUTH_REFRESH,
    DEFAULT_TIMEOUT,
    TOKEN_KEY,
    REFRESH_KEY,
    USER_KEY,
    CSRFTOKEN_KEY
} from "../utils/const.js";

class AuthService {
    constructor() {
        this.api = new ApiClient(URL_BASE, {
            timeout: DEFAULT_TIMEOUT,
            refreshEndpoint: URL_AUTH_REFRESH,
            onUnauthorized: () => this.logout()
        });

        // Suscribirse a cambios de token para persistirlos automáticamente
        this.api.subscribe((newToken) => {
            if (newToken) {
                localStorage.setItem(TOKEN_KEY, newToken);
            }
        });

        this.initializeFromStorage();
    }

    // Obtiene la instancia del cliente API
    getApiClient() {
        return this.api;
    }

    // Obtiene el token CSRF de las cookies
    getCsrfToken() {
        let cookieValue = null;

        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');

            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();

                if (cookie.substring(0, CSRFTOKEN_KEY.length + 1) === (CSRFTOKEN_KEY + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(CSRFTOKEN_KEY.length + 1));
                    break;
                }
            }
        }

        return cookieValue;
    }

    // Extrae información del usuario desde el payload del JWT
    getUserFromToken(token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));

            return {
                userId: payload.user_id,
                email: payload.email || payload.sub
            };
        } catch (error) {
            return null;
        }
    }

    // Inicializa los tokens desde el almacenamiento local
    initializeFromStorage() {
        const token = localStorage.getItem(TOKEN_KEY);
        const refresh = localStorage.getItem(REFRESH_KEY);

        if (token) {
            this.api.setToken(token);
        }

        if (refresh) {
            this.api.setRefreshToken(refresh);
        }

        const csrfToken = this.getCsrfToken();

        if (csrfToken) {
            this.api.setCsrfToken(csrfToken);
        }
    }

    // Verifica si el usuario está autenticado
    isAuthenticated() {
        const token = localStorage.getItem(TOKEN_KEY);
        return token && !this.isTokenExpired(token);
    }

    // Verifica si un token JWT ha expirado
    isTokenExpired(token) {
        if (!token) {
            return true;
        }

        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const exp = payload.exp * 1000;
            return Date.now() >= exp;
        } catch (e) {
            return true;
        }
    }

    // Realiza el inicio de sesión
    async login(email, password) {
        try {
            // Desactivar reintento de refresco para el login para evitar bucles con tokens viejos
            const response = await this.api.post(URL_AUTH_TOKEN,
                { email, password },
                { retryRefresh: false }
            );

            if (!response.data || !response.data.access) {
                throw new Error('La respuesta del servidor es inválida (Tokens faltantes).');
            }

            const accessToken = response.data.access;
            const refreshToken = response.data.refresh;

            this.api.setToken(accessToken);
            this.api.setRefreshToken(refreshToken);

            const csrfToken = this.getCsrfToken();
            if (csrfToken) {
                this.api.setCsrfToken(csrfToken);
            }

            localStorage.setItem(TOKEN_KEY, accessToken);
            localStorage.setItem(REFRESH_KEY, refreshToken);

            // Guardar info básica del usuario si está disponible
            const user = this.getUserFromToken(accessToken);
            if (user) {
                localStorage.setItem(USER_KEY, JSON.stringify(user));
            }

            return { success: true, user }
        } catch (error) {
            throw error;
        }
    }

    // Cierra la sesión y limpia el almacenamiento
    logout() {
        this.api.clearTokens();
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(REFRESH_KEY);
        localStorage.removeItem(USER_KEY);
    }
}

export const authService = new AuthService();
