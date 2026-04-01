import { authService } from "./AuthService.js";
import {
    URL_PURCHASE_RETURNS,
    URL_COMPLETED_PURCHASE_RETURNS,
    URL_CANCELED_PURCHASE_RETURNS,
} from "../util/const.js";

class PurchaseReturnService {
    get api() {
        return authService.getApiClient();
    }

    async getAllPurchaseReturns(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_PURCHASE_RETURNS}?${params}` : `${URL_PURCHASE_RETURNS}`;
        return await this.api.get(endpoint);
    }

    async getPurchaseReturnById(id) {
        return await this.api.get(`${URL_PURCHASE_RETURNS}${id}/`);
    }

    async create(dades) {
        return await this.api.post(`${URL_PURCHASE_RETURNS}`, dades);
    }

    async update(id, dades) {
        return await this.api.patch(`${URL_PURCHASE_RETURNS}${id}/`, dades);
    }

    async delete(id) {
        return await this.api.delete(`${URL_PURCHASE_RETURNS}${id}/`);
    }

    async cancel(id) {
        return await this.api.patch(`${URL_PURCHASE_RETURNS}${id}/cancel/`);
    }

    async getDetailsPurchaseReturnById(id) {
        return await this.api.get(`${URL_PURCHASE_RETURNS}${id}/details/`);
    }

    async getDetailPurchaseReturnById(purchase_return_id, detail_return_id) {
        return await this.api.get(`${URL_PURCHASE_RETURNS}${purchase_return_id}/details/${detail_return_id}/`);
    }

    async getCompletedPurchaseReturns() {
        return await this.api.get(`${URL_COMPLETED_PURCHASE_RETURNS}`);
    }

    async getCanceledPurchaseReturns() {
        return await this.api.get(`${URL_CANCELED_PURCHASE_RETURNS}`);
    }
}

export const purchaseReturnService = new PurchaseReturnService();
