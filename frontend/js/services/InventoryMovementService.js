import { authService } from "./AuthService.js";
import {
    URL_INVENTORY_MOVEMENTS,
} from "../util/const.js";

class InventoryMovementService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getAllInventoryMovements(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_INVENTORY_MOVEMENTS}?${params}` : `${URL_INVENTORY_MOVEMENTS}`;
        return await this.api.get(endpoint);
    }

    async getInventoryMovementById(id) {
        return await this.api.get(`${URL_INVENTORY_MOVEMENTS}${id}/`);
    }
}

export const inventoryMovementService = new InventoryMovementService();
