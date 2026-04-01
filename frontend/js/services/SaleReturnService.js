import { authService } from "./AuthService.js";
import {
    URL_SALE_RETURNS,
    URL_COMPLETED_SALE_RETURNS,
    URL_CANCELED_SALE_RETURNS,
} from "../util/const.js";

class SaleReturnService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getAllSaleReturns(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_SALE_RETURNS}?${params}` : `${URL_SALE_RETURNS}`;
        return await this.api.get(endpoint);
    }

    async getSaleReturnById(id) {
        return await this.api.get(`${URL_SALE_RETURNS}${id}/`);
    }

    async create(dades) {
        return await this.api.post(`${URL_SALE_RETURNS}`, dades);
    }

    async update(id, dades) {
        return await this.api.patch(`${URL_SALE_RETURNS}${id}/`, dades);
    }

    async delete(id) {
        return await this.api.delete(`${URL_SALE_RETURNS}${id}/`);
    }

    async cancel(id) {
        return await this.api.patch(`${URL_SALE_RETURNS}${id}/cancel/`);
    }

    async getDetailsSaleReturnById(id) {
        return await this.api.get(`${URL_SALE_RETURNS}${id}/details/`);
    }

    async getDetailSaleReturnById(sale_return_id, detail_return_id) {
        return await this.api.get(`${URL_SALE_RETURNS}${sale_return_id}/details/${detail_return_id}/`);
    }

    async getCompletedSaleReturns() {
        return await this.api.get(`${URL_COMPLETED_SALE_RETURNS}`);
    }

    async getCanceledSaleReturns() {
        return await this.api.get(`${URL_CANCELED_SALE_RETURNS}`);
    }
}

export const saleReturnService = new SaleReturnService();
