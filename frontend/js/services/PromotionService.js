import { authService } from "./AuthService.js";
import {
    URL_PROMOTIONS,
    URL_ACTIVE_PROMOTIONS,
    URL_INACTIVE_PROMOTIONS,
} from "../util/const.js";

class PromotionService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getAllPromotions(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_PROMOTIONS}?${params}` : `${URL_PROMOTIONS}`;
        return await this.api.get(endpoint);
    }

    async getPromootionById(id) {
        return await this.api.get(`${URL_PROMOTIONS}${id}/`);
    }

    async create(dades) {
        return await this.api.post(`${URL_PROMOTIONS}`, dades);
    }

    async update(id, dades) {
        return await this.api.patch(`${URL_PROMOTIONS}${id}/`, dades);
    }

    async delete(id) {
        return await this.api.delete(`${URL_PROMOTIONS}${id}/`);
    }

    async activate(id) {
        return await this.api.patch(`${URL_PROMOTIONS}${id}/activate/`);
    }

    async deactivate(id) {
        return await this.api.patch(`${URL_PROMOTIONS}${id}/deactivate/`);
    }

    async getActivePromotions() {
        return await this.api.get(`${URL_ACTIVE_PROMOTIONS}`);
    }

    async getInactivePromotions() {
        return await this.api.get(`${URL_INACTIVE_PROMOTIONS}`);
    }
}

export const promotionService = new PromotionService();
