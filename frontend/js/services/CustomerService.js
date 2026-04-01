import { authService } from "./AuthService.js";
import {
    URL_CUSTOMERS,
    URL_ACTIVE_CUSTOMERS,
    URL_INACTIVE_CUSTOMERS,
} from "../util/const.js";

class CustomerService {
    get api() {
        return authService.getApiClient();
    }

    async getAllCustomers(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_CUSTOMERS}?${params}` : `${URL_CUSTOMERS}`;
        return await this.api.get(endpoint);
    }

    async getCustomerById(id) {
        return await this.api.get(`${URL_CUSTOMERS}${id}/`);
    }

    async create(dades) {
        return await this.api.post(`${URL_CUSTOMERS}`, dades);
    }

    async update(id, dades) {
        return await this.api.patch(`${URL_CUSTOMERS}${id}/`, dades);
    }

    async delete(id) {
        return await this.api.delete(`${URL_CUSTOMERS}${id}/`);
    }

    async activate(id) {
        return await this.api.patch(`${URL_CUSTOMERS}${id}/activate/`);
    }

    async deactivate(id) {
        return await this.api.patch(`${URL_CUSTOMERS}${id}/deactivate/`);
    }

    async getActiveCustomers() {
        return await this.api.get(`${URL_ACTIVE_CUSTOMERS}`);
    }

    async getInactiveCustomers() {
        return await this.api.get(`${URL_INACTIVE_CUSTOMERS}`);
    }

    async getListPromotions(id) {
        return await this.api.get(`${URL_CUSTOMERS}${id}/list-promotions`);
    }
}

export const customerService = new CustomerService();
