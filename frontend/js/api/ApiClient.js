// Cliente HTTP para comunicaciones con el backend
// Gestiona autenticación, reintentos y manejo de errores

import { DEFAULT_TIMEOUT, URL_AUTH_REFRESH } from '../utils/const.js';

// Error personalizado para respuestas HTTP fallidas
export class ApiClientError extends Error {
    constructor(message, status, data) {
        super(message);
        this.name = 'ApiClientError';
        this.status = status;
        this.data = data;
    }
}

// Cliente HTTP con soporte para JWT, CSRF y reintentos automáticos
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

    // Configura token CSRF
    setCsrfToken(token) {
        this.csrfToken = token;
    }

    // Configura token de acceso JWT
    setToken(token) {
        this.authToken = token;
    }

    // Configura token de refresco JWT
    setRefreshToken(token) {
        this.refreshToken = token;
    }

    // Limpia todos los tokens almacenados
    clearTokens() {
        this.authToken = null;
        this.refreshToken = null;
    }

    // Registra callback para notificaciones de token renovado
    subscribe(callback) {
        this.subscribers.push(callback);
    }

    // Notifica a todos los suscriptores del nuevo token
    notifySubscribers(token) {
        this.subscribers.forEach(cb => cb(token));
    }

    // Renueva el token de acceso usando el refresh token
    async refreshAccessToken() {
        // Si ya hay un refresco en curso, esperar a que termine
        if (this.isRefreshing) {
            return new Promise((resolve) => {
                this.subscribers.push((token) => resolve(token));
            });
        }

        this.isRefreshing = true;

        try {
            const response = await fetch(`${this.baseUrl}${this.refreshEndpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: this.refreshToken }),
            });

            if (!response.ok) {
                throw new ApiClientError('Error al renovar la sesión', response.status);
            }

            const data = await response.json();
            this.authToken = data.access;
            this.notifySubscribers(data.access);
            return data.access;
        } finally {
            this.isRefreshing = false;
        }
    }

    // Construye cabeceras HTTP para la petición
    buildHeaders(additionalHeaders = {}, needsCsrf = false, isFormData = false) {
        const headers = { ...additionalHeaders };

        if (!isFormData && !headers['Content-Type']) {
            headers['Content-Type'] = 'application/json';
        }

        if (this.authToken) {
            headers['Authorization'] = `Bearer ${this.authToken}`;
        }

        if (needsCsrf && this.csrfToken) {
            headers['X-CSRFTOKEN'] = this.csrfToken;
        }

        return headers;
    }

    // Ejecuta una petición HTTP con deduplicación y timeout
    async request(endpoint, options = {}) {
        const {
            method = 'GET',
            data = null,
            headers = {},
            timeout = this.timeout,
            retryRefresh = true,
            responseType = 'json',
        } = options;

        // Evitar peticiones duplicadas simultáneas
        const requestKey = `${method}:${endpoint}:${JSON.stringify(data || {})}`;

        if (this.pendingRequests.has(requestKey)) {
            return this.pendingRequests.get(requestKey);
        }

        const isFormData = data instanceof FormData;
        const needsCsrf = ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method);
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            method,
            headers: this.buildHeaders(headers, needsCsrf, isFormData),
        };

        if (data && ['POST', 'PUT', 'PATCH'].includes(method)) {
            config.body = isFormData ? data : JSON.stringify(data);
        }

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        const fetchPromise = this._executeRequest(url, config, needsCsrf, retryRefresh, timeoutId, controller, responseType);

        this.pendingRequests.set(requestKey, fetchPromise);

        try {
            return await fetchPromise;
        } finally {
            this.pendingRequests.delete(requestKey);
        }
    }

    // Ejecuta la petición con manejo de 401 y reintentos
    async _executeRequest(url, config, needsCsrf, retryRefresh, timeoutId, controller, responseType) {
        config.signal = controller.signal;

        try {
            const response = await fetch(url, config);
            clearTimeout(timeoutId);

            // Intentar renovar token si expiró
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
                    return this.handleResponse(retryResponse, responseType);
                } catch (refreshError) {
                    this.clearTokens();

                    if (this.onUnauthorized) {
                        this.onUnauthorized();
                    }

                    throw new ApiClientError('Su sesión ha caducado por seguridad. Por favor, vuelve a iniciar sesión.', 401);
                }
            }

            return this.handleResponse(response, responseType);
        } catch (error) {
            clearTimeout(timeoutId);

            if (error.name === 'AbortError') {
                throw new ApiClientError('La solicitud ha tardado demasiado tiempo. Por favor, revisa tu conexión a internet.', 408);
            }

            // Capturar errores de red (como "Failed to fetch")
            if (error instanceof TypeError && error.message.toLowerCase().includes('fetch')) {
                throw new ApiClientError('No se pudo establecer conexión con el servidor. Revisa tu conexión a internet o intenta más tarde.', 503);
            }

            throw error;
        }
    }

    // Procesa la respuesta HTTP y extrae datos o errores
    async handleResponse(response, responseType = 'json') {
        const contentType = response.headers.get('content-type');
        let data = null;

        if (responseType === 'blob') {
            data = await response.blob().catch(() => null);
        } else if (contentType && contentType.includes('application/json')) {
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
            data,
        };

        if (response.status === 204 || !data) {
            return { ...successResponse, data: null };
        }

        return successResponse;
    }

    // Extrae mensaje legible de errores HTTP y validación DRF
    extractErrorMessage(data, status) {
        const statusMessages = {
            400: 'Los datos enviados no son válidos. Por favor, revisa la información ingresada.',
            401: 'Usuario o contraseña incorrectos. Verifica tus credenciales.',
            403: 'No tienes permisos suficientes para realizar esta acción.',
            404: 'El recurso solicitado no está disponible actualmente.',
            405: 'Esta operación no está permitida por el sistema.',
            408: 'La conexión es demasiado lenta. Revisa tu internet.',
            429: 'Has realizado demasiadas solicitudes. Espera un momento antes de reintentar.',
            500: 'Error interno en el servidor. Estamos trabajando para solucionarlo.',
            502: 'El servidor de Nexus Inventory no responde temporalmente.',
            503: 'El servicio no está disponible en este momento. Inténtalo más tarde.',
            504: 'El servidor ha tardado demasiado en procesar tu solicitud.',
        };

        const detailTranslations = {
            'authentication credentials were not provided.': 'No se proporcionaron credenciales de acceso.',
            'no active account found with the given credentials': 'No se encontró ninguna cuenta activa con estas credenciales.',
            'token is invalid or expired': 'Tu sesión es inválida o ha caducado.',
            'given token not valid for any token type': 'El acceso no es válido. Por favor, inicia sesión de nuevo.',
            'you do not have permission to perform this action.': 'No tienes los permisos necesarios para esta acción.',
            'not found.': 'Lo sentimos, el recurso no existe.',
            'method "post" not allowed.': 'No se permite enviar datos en esta sección.',
            'method "get" not allowed.': 'No se permite consultar datos en esta sección.',
        };

        if (!data) {
            return statusMessages[status] || `Error de conexión (Código: ${status})`;
        }

        if (typeof data === 'string') {
            return data;
        }

        // Errores de validación de campos Django (formato errors)
        if (data.errors && typeof data.errors === 'object') {
            const firstField = Object.keys(data.errors)[0];
            const firstError = Object.values(data.errors)[0];
            const fieldName = firstField.charAt(0).toUpperCase() + firstField.slice(1);

            if (Array.isArray(firstError)) {
                return `${fieldName}: ${firstError[0]}`;
            }
            return `${fieldName}: ${firstError}`;
        }

        // Error simple con campo detail
        if (data.detail) {
            const detailLower = data.detail.toLowerCase();
            return detailTranslations[detailLower] || data.detail;
        }

        if (data.message) {
            return data.message;
        }

        // Errores de campos no específicos
        if (data.non_field_errors) {
            return data.non_field_errors[0];
        }

        // Errores de validación directamente en el objeto (formato DRF por defecto)
        if (typeof data === 'object' && Object.keys(data).length > 0) {
            const messages = [];
            for (const [field, errors] of Object.entries(data)) {
                if (Array.isArray(errors)) {
                    const fieldName = field.match(/^\d+$/) ? 'Detalle' : field.charAt(0).toUpperCase() + field.slice(1);
                    messages.push(`${fieldName}: ${errors.join(', ')}`);
                } else if (typeof errors === 'object' && errors !== null) {
                    const fieldName = field.match(/^\d+$/) ? 'Detalle' : field.charAt(0).toUpperCase() + field.slice(1);
                    for (const [index, fieldErrors] of Object.entries(errors)) {
                        if (typeof fieldErrors === 'object' && fieldErrors !== null) {
                            for (const [subField, subErrors] of Object.entries(fieldErrors)) {
                                if (Array.isArray(subErrors)) {
                                    const subFieldName = subField.charAt(0).toUpperCase() + subField.slice(1);
                                    messages.push(`${fieldName} ${subFieldName}: ${subErrors.join(', ')}`);
                                } else if (typeof subErrors === 'string') {
                                    const subFieldName = subField.charAt(0).toUpperCase() + subField.slice(1);
                                    messages.push(`${fieldName} ${subFieldName}: ${subErrors}`);
                                }
                            }
                        } else if (typeof fieldErrors === 'string') {
                            messages.push(`${fieldName}: ${fieldErrors}`);
                        }
                    }
                }
            }
            if (messages.length > 0) {
                return messages.join('. ');
            }
        }

        return statusMessages[status] || `Error inesperado (${status})`;
    }

    // Devuelve mensaje de éxito según código HTTP
    getSuccessMessage(status) {
        const messages = {
            200: 'Operación exitosa',
            201: 'Recurso creado correctamente',
            204: 'Operación exitosa',
        };
        return messages[status] || 'Operación exitosa';
    }

    // Petición GET
    get(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'GET' });
    }

    // Petición POST
    async post(endpoint, data, options = {}) {
        return await this.request(endpoint, { ...options, method: 'POST', data });
    }

    // Petición PATCH
    async patch(endpoint, data, options = {}) {
        return await this.request(endpoint, { ...options, method: 'PATCH', data });
    }

    // Petición DELETE
    async delete(endpoint, options = {}) {
        return await this.request(endpoint, { ...options, method: 'DELETE' });
    }
}
