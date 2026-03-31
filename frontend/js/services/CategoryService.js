import { authService } from "./AuthService.js";
import {
    URL_CATEGORIES,
    URL_ACTIVE_CATEGORIES,
    URL_INACTIVE_CATEGORIES,
} from "../util/const.js";

class CategoryService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getAllCategories(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_CATEGORIES}?${params}` : `${URL_CATEGORIES}`;
        return await this.api.get(endpoint);
    }

    async getCategoryById(id) {
        return await this.api.get(`${URL_CATEGORIES}${id}/`);
    }

    async create(dades) {
        return await this.api.post(`${URL_CATEGORIES}`, dades);
    }

    async update(id, dades) {
        return await this.api.patch(`${URL_CATEGORIES}${id}/`, dades);
    }

    async delete(id) {
        return await this.api.delete(`${URL_CATEGORIES}${id}/`);
    }

    async activate(id) {
        return await this.api.patch(`${URL_CATEGORIES}${id}/activate/`);
    }

    async deactivate(id) {
        return await this.api.patch(`${URL_CATEGORIES}${id}/deactivate/`);
    }

    async getActiveCategories() {
        return await this.api.get(`${URL_ACTIVE_CATEGORIES}`);
    }

    async getInactiveCategories() {
        return await this.api.get(`${URL_INACTIVE_CATEGORIES}`);
    }
}

export const categoryService = new CategoryService();
