import { authService } from "./AuthService.js";
import { URL_CUSTOMER_PROMOTIONS } from "../util/const.js";

class CustomerPromotionService {
    get api() {
        return authService.getApiClient();
    }

    async getAllCustomerPromotions(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_CUSTOMER_PROMOTIONS}?${params}` : `${URL_CUSTOMER_PROMOTIONS}`;
        return await this.api.get(endpoint);
    }

    async getCustomerPromotionById(id) {
        return await this.api.get(`${URL_CUSTOMER_PROMOTIONS}${id}/`);
    }

    async create(dades) {
        return await this.api.post(`${URL_CUSTOMER_PROMOTIONS}`, dades);
    }

    async update(id, dades) {
        return await this.api.patch(`${URL_CUSTOMER_PROMOTIONS}${id}/`, dades);
    }

    async delete(id) {
        return await this.api.delete(`${URL_CUSTOMER_PROMOTIONS}${id}/`);
    }

    async apply(id) {
        return await this.api.patch(`${URL_CUSTOMER_PROMOTIONS}${id}/apply/`);
    }
}

export const customerPromotionService = new CustomerPromotionService();
