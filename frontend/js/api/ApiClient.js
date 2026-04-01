/**
 * ========================================
 * MÓDULO DE BASE DE API
 * ========================================
 * Gestión de comunicaciones con el backend
 * Utiliza fetch para las peticiones HTTP
 * ========================================
 */

import { DEFAULT_TIMEOUT, URL_AUTH_REFRESH } from "../util/const.js";

export class ApiClientError extends Error {
    constructor(message, status, data) {
        super(message);
        this.name = "ApiClientError";
        this.status = status;
        this.data = data;
    }
}

export class ApiClient {
    constructor(baseUrl, options = {}) {
        this.baseUrl = baseUrl;
        this.timeout = options.timeout || DEFAULT_TIMEOUT;
        this.authToken = options.authToken || null;
        this.refreshToken = options.refreshToken || null;
        this.csrfToken = options.csrfToken || null;
        this.refreshEndpoint = options.refreshEndpoint || URL_AUTH_REFRESH;
        this.onUnauthorized = options.onUnauthorized || null;
        this.isRefreshing = false;
        this.subscribers = [];
        this.pendingRequests = new Map();
    }

    setCsrfToken(token) {
        this.csrfToken = token;
    }

    setToken(token) {
        this.authToken = token;
    }

    setRefreshToken(token) {
        this.refreshToken = token;
    }

    clearTokens() {
        this.authToken = null;
        this.refreshToken = null;
    }

    subscribe(callback) {
        this.subscribers.push(callback);
    }

    notifySubscribers(token) {
        this.subscribers.forEach(cb => cb(token));
    }

    async refreshAccessToken() {
        if (this.isRefreshing) {
            return new Promise((resolve) => {
                this.subscribers.push((token) => resolve(token));
            });
        }

        this.isRefreshing = true;

        try {
            const response = await fetch(`${this.baseUrl}${this.refreshEndpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh: this.refreshToken }),
            });

            if (!response.ok) {
                throw new ApiClientError('Token refresh failed', response.status);
            }

            const data = await response.json();
            this.authToken = data.access;
            this.notifySubscribers(data.access);
            return data.access;
        } finally {
            this.isRefreshing = false;
        }
    }

    buildHeaders(additionalHeaders = {}, needsCsrf = false) {
        const headers = {
            'Content-Type': 'application/json',
            ...additionalHeaders,
        };

        if (this.authToken) {
            headers['Authorization'] = `Bearer ${this.authToken}`;
        }

        if (needsCsrf && this.csrfToken) {
            headers['X-CSRFTOKEN'] = this.csrfToken;
        }

        return headers;
    }

    async request(endpoint, options = {}) {
        const {
            method = 'GET',
            data = null,
            headers = {},
            timeout = this.timeout,
            retryRefresh = true,
        } = options;

        const requestKey = `${method}:${endpoint}:${JSON.stringify(data || {})}`;

        if (this.pendingRequests.has(requestKey)) {
            return this.pendingRequests.get(requestKey);
        }

        const needsCsrf = ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method);
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            method,
            headers: this.buildHeaders(headers, needsCsrf),
        };

        if (data && ['POST', 'PUT', 'PATCH'].includes(method)) {
            config.body = JSON.stringify(data);
        }

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        const fetchPromise = this._executeRequest(url, config, needsCsrf, retryRefresh, timeoutId, controller);

        this.pendingRequests.set(requestKey, fetchPromise);

        try {
            return await fetchPromise;
        } finally {
            this.pendingRequests.delete(requestKey);
        }
    }

    async _executeRequest(url, config, needsCsrf, retryRefresh, timeoutId, controller) {
        config.signal = controller.signal;

        try {
            const response = await fetch(url, config);
            clearTimeout(timeoutId);

            if (response.status === 401 && retryRefresh && this.refreshToken) {
                try {
                    const newToken = await this.refreshAccessToken();
                    const retryConfig = {
                        ...config,
                        headers: {
                            ...config.headers,
                            'Authorization': `Bearer ${newToken}`,
                        },
                    };

                    if (needsCsrf && this.csrfToken) {
                        retryConfig.headers['X-CSRFTOKEN'] = this.csrfToken;
                    }

                    const retryResponse = await fetch(url, retryConfig);

                    return this.handleResponse(retryResponse);
                } catch (refreshError) {
                    this.clearTokens();

                    if (this.onUnauthorized) {
                        this.onUnauthorized();
                    }

                    throw new ApiClientError('Session expired', 401);
                }
            }

            return this.handleResponse(response);
        } catch (error) {
            clearTimeout(timeoutId);

            if (error.name === 'AbortError') {
                throw new ApiClientError('Request timeout', 408);
            }
            throw error;
        }
    }

    async handleResponse(response) {
        const contentType = response.headers.get('content-type');
        let data = null;

        if (contentType && contentType.includes('application/json')) {
            data = await response.json().catch(() => null);
        }

        if (!response.ok) {
            const message = this.extractErrorMessage(data, response.status);
            throw new ApiClientError(message, response.status, data);
        }

        const successResponse = {
            success: true,
            status: response.status,
            message: this.getSuccessMessage(response.status),
            data: data
        };

        if (response.status === 204 || !data) {
            return { ...successResponse, data: null };
        }

        return successResponse;
    }

    extractErrorMessage(data, status) {
        if (!data) {
            return `HTTP error ${status}`;
        }

        if (typeof data === 'string') {
            return data;
        }

        if (data.detail) {
            return data.detail;
        }

        if (data.message) {
            return data.message;
        }

        if (data.errors && typeof data.errors === 'object') {
            const firstError = Object.values(data.errors)[0];
            if (Array.isArray(firstError)) {
                return firstError[0];
            }
            return JSON.stringify(firstError);
        }

        if (data.non_field_errors) {
            return data.non_field_errors[0];
        }

        return `HTTP error ${status}`;
    }

    getSuccessMessage(status) {
        const messages = {
            200: 'Operación exitosa',
            201: 'Recurso creado correctamente',
            204: 'Operación exitosa',
        };
        return messages[status] || 'Operación exitosa';
    }

    get(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'GET' });
    }

    post(endpoint, data, options = {}) {
        return this.request(endpoint, { ...options, method: 'POST', data });
    }

    patch(endpoint, data, options = {}) {
        return this.request(endpoint, { ...options, method: 'PATCH', data });
    }

    delete(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'DELETE' });
    }
}
