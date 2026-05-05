// Servicio base con métodos CRUD genéricos

import { authService } from "./AuthService.js";

export class BaseService {
    // Configura el endpoint base
    constructor(endpoint) {
        this.endpoint = endpoint;
    }

    get api() {
        return authService.getApiClient();
    }

    // Activa un registro
    async activate(id) {
        return await this.api.patch(`${this.endpoint}${id}/activate/`);
    }

    // Crea un nuevo registro
    async create(data) {
        return await this.api.post(this.endpoint, data);
    }

    // Desactiva un registro
    async deactivate(id) {
        return await this.api.patch(`${this.endpoint}${id}/deactivate/`);
    }

    // Obtiene todos los registros con filtros opcionales
    async getAll(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const url = params ? `${this.endpoint}?${params}` : `${this.endpoint}`;
        return await this.api.get(url);
    }

    // Actualiza un registro
    async update(id, data) {
        return await this.api.patch(`${this.endpoint}${id}/`, data);
    }
}
