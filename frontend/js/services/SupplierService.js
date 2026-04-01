import { authService } from "./AuthService.js";
import {
    URL_SUPPLIERS,
    URL_ACTIVE_SUPPLIERS,
    URL_INACTIVE_SUPPLIERS,
} from "../util/const.js";

class SupplierService {
    get api() {
        return authService.getApiClient();
    }

    async getAllSuppliers(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_SUPPLIERS}?${params}` : `${URL_SUPPLIERS}`;
        return await this.api.get(endpoint);
    }

    async getSupplierById(id) {
        return await this.api.get(`${URL_SUPPLIERS}${id}/`);
    }

    async create(dades) {
        return await this.api.post(`${URL_SUPPLIERS}`, dades);
    }

    async update(id, dades) {
        return await this.api.patch(`${URL_SUPPLIERS}${id}/`, dades);
    }

    async delete(id) {
        return await this.api.delete(`${URL_SUPPLIERS}${id}/`);
    }

    async activate(id) {
        return await this.api.patch(`${URL_SUPPLIERS}${id}/activate/`);
    }

    async deactivate(id) {
        return await this.api.patch(`${URL_SUPPLIERS}${id}/deactivate/`);
    }

    async getActiveSuppliers() {
        return await this.api.get(`${URL_ACTIVE_SUPPLIERS}`);
    }

    async getInactiveSuppliers() {
        return await this.api.get(`${URL_INACTIVE_SUPPLIERS}`);
    }
}

export const supplierService = new SupplierService();
