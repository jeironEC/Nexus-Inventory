import { authService } from "./AuthService.js";
import {
    URL_INVENTORIES,
    URL_LOW_INVENTORIES,
    URL_PRODUCT_INVENTORIES,
} from "../util/const.js";

class InventoryService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getAllInventories(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_INVENTORIES}?${params}` : `${URL_INVENTORIES}`;
        return await this.api.get(endpoint);
    }

    async getLowInventory() {
        return await this.api.get(`${URL_LOW_INVENTORIES}`);
    }

    async getProductInventory(id) {
        return await this.api.get(`${URL_PRODUCT_INVENTORIES}${id}/`);
    }
}

export const inventoryService = new InventoryService();
