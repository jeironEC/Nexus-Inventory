import { authService } from "./AuthService.js";
import {
    URL_PRODUCTS,
    URL_ACTIVE_PRODUCTS,
    URL_INACTIVE_PRODUCTS,
} from "../util/const.js";

class ProductService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getAllProducts(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_PRODUCTS}?${params}` : `${URL_PRODUCTS}`;
        return await this.api.get(endpoint);
    }

    async getProductById(id) {
        return await this.api.get(`${URL_PRODUCTS}${id}/`);
    }

    async create(dades) {
        return await this.api.post(`${URL_PRODUCTS}`, dades);
    }

    async update(id, dades) {
        return await this.api.patch(`${URL_PRODUCTS}${id}/`, dades);
    }

    async delete(id) {
        return await this.api.delete(`${URL_PRODUCTS}${id}/`);
    }

    async activate(id) {
        return await this.api.patch(`${URL_PRODUCTS}${id}/activate/`);
    }

    async deactivate(id) {
        return await this.api.patch(`${URL_PRODUCTS}${id}/deactivate/`);
    }

    async getActiveProducts() {
        return await this.api.get(`${URL_ACTIVE_PRODUCTS}`);
    }

    async getInactiveProducts() {
        return await this.api.get(`${URL_INACTIVE_PRODUCTS}`);
    }
}

export const productService = new ProductService();
