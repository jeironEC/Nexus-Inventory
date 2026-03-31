import { authService } from "./AuthService.js";
import {
    URL_PURCHASES,
    URL_COMPLETED_PURCHASES,
    URL_CANCELED_PURCHASES,
} from "../util/const.js";

class PurchaseService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getAllPurchases(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_PURCHASES}?${params}` : `${URL_PURCHASES}`;
        return await this.api.get(endpoint);
    }

    async getPurchaseById(id) {
        return await this.api.get(`${URL_PURCHASES}${id}/`);
    }

    async create(dades) {
        return await this.api.post(`${URL_PURCHASES}`, dades);
    }

    async update(id, dades) {
        return await this.api.patch(`${URL_PURCHASES}${id}/`, dades);
    }

    async delete(id) {
        return await this.api.delete(`${URL_PURCHASES}${id}/`);
    }

    async cancel(id) {
        return await this.api.patch(`${URL_PURCHASES}${id}/cancel/`);
    }

    async getDetailsPurchaseById(id) {
        return await this.api.get(`${URL_PURCHASES}${id}/details/`);
    }

    async getDetailPurchaseById(purchase_id, detail_id) {
        return await this.api.get(`${URL_PURCHASES}${purchase_id}/details/${detail_id}/`);
    }

    async getCompletedPurchases() {
        return await this.api.get(`${URL_COMPLETED_PURCHASES}`);
    }

    async getCanceledPurchases() {
        return await this.api.get(`${URL_CANCELED_PURCHASES}`);
    }
}

export const purchaseService = new PurchaseService();
