import { authService } from "./AuthService.js";
import {
    URL_SALES,
    URL_COMPLETED_SALES,
    URL_CANCELED_SALES,
} from "../util/const.js";

class SaleService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getAllSales(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_SALES}?${params}` : `${URL_SALES}`;
        return await this.api.get(endpoint);
    }

    async getSaleById(id) {
        return await this.api.get(`${URL_SALES}${id}/`);
    }

    async create(dades) {
        return await this.api.post(`${URL_SALES}`, dades);
    }

    async update(id, dades) {
        return await this.api.patch(`${URL_SALES}${id}/`, dades);
    }

    async delete(id) {
        return await this.api.delete(`${URL_SALES}${id}/`);
    }

    async cancel(id) {
        return await this.api.patch(`${URL_SALES}${id}/cancel/`);
    }

    async getDetailsSaleById(id) {
        return await this.api.get(`${URL_SALES}${id}/details/`);
    }

    async getDetailSaleById(sale_id, detail_id) {
        return await this.api.get(`${URL_SALES}${sale_id}/details/${detail_id}/`);
    }

    async getCompletedSales() {
        return await this.api.get(`${URL_COMPLETED_SALES}`);
    }

    async getCanceledSales() {
        return await this.api.get(`${URL_CANCELED_SALES}`);
    }
}

export const saleService = new SaleService();
