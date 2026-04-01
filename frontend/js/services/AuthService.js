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
} from "../util/const.js";

class AuthService {
    constructor() {
        this.api = new ApiClient(URL_BASE, {
            timeout: DEFAULT_TIMEOUT,
            refreshEndpoint: URL_AUTH_REFRESH,
            onUnauthorized: () => this.logout()
        });
        this.initializeFromStorage();
    }

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

    async login(email, password) {
        try {
            const response = await this.api.post(URL_AUTH_TOKEN, { email, password });

            const accessToken = response.data.access;
            const refreshToken = response.data.refresh;

            this.setToken(accessToken);
            this.setRefreshToken(refreshToken);
            this.setCsrfToken(this.getCsrfToken());

            localStorage.setItem(TOKEN_KEY, accessToken);
            localStorage.setItem(REFRESH_KEY, refreshToken);

            return { success: true, user: this.getUserFromToken(accessToken) }
        } catch (error) {
            throw error;
        }
    }

    logout() {
        this.api.clearTokens();
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(REFRESH_KEY);
        localStorage.removeItem(USER_KEY);
    }

    async refreshToken() {
        const refresh = localStorage.getItem(REFRESH_KEY);

        if (!refresh) {
            throw new Error('No refresh token available');
        }

        try {
            const response = await this.api.post(URL_AUTH_REFRESH, { refresh });

            const accessToken = response.data.access;
            this.setToken(accessToken);
            localStorage.setItem(TOKEN_KEY, accessToken);

            return accessToken;
        } catch (error) {
            this.logout();
            throw error;
        }
    }

    isAuthenticated() {
        const token = localStorage.getItem(TOKEN_KEY);
        return token && !this.isTokenExpired(token);
    }

    getToken() {
        return localStorage.getItem(TOKEN_KEY);
    }

    setToken(token) {
        this.api.setToken(token);
    }

    setRefreshToken(token) {
        this.api.setRefreshToken(token);
    }

    setCsrfToken(token) {
        this.api.setCsrfToken(token);
    }

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

    getApiClient() {
        return this.api;
    }
}

export const authService = new AuthService();
