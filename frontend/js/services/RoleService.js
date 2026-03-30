import { authService } from "./AuthService.js";
import {
    URL_ROLE,
    URL_ACTIVE_ROLES,
    URL_INACTIVE_ROLES,
} from "../util/const.js";

export class RoleService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getAllRoles(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_ROLE}?${params}` : `${URL_ROLE}`;
        return await this.api.get(endpoint);
    }

    async getRoleById(id) {
        return await this.api.get(`${URL_ROLE}${id}/`);
    }

    async create(dades) {
        return await this.api.post(`${URL_ROLE}`, dades);
    }

    async update(id, dades) {
        return await this.api.patch(`${URL_ROLE}${id}/`, dades);
    }

    async delete(id) {
        return await this.api.delete(`${URL_ROLE}${id}/`);
    }

    async activate(id) {
        return await this.api.patch(`${URL_ROLE}${id}/activate/`);
    }

    async deactivate(id) {
        return await this.api.patch(`${URL_ROLE}${id}/deactivate/`);
    }

    async getActiveRoles() {
        return await this.api.get(`${URL_ACTIVE_ROLES}`);
    }

    async getInactiveRoles() {
        return await this.api.get(`${URL_INACTIVE_ROLES}`);
    }
}

export const roleService = new RoleService();
