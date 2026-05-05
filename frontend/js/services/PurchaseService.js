// Servicio para gestionar compras

import { BaseService } from "./BaseService.js";
import { URL_PURCHASES } from "../utils/const.js";

class PurchaseService extends BaseService {
    constructor() {
        super(URL_PURCHASES);
    }

    // Cancela una compra
    async cancel(id) {
        return await this.api.patch(`${URL_PURCHASES}${id}/cancel/`);
    }

    // Obtiene los detalles de una compra por su ID
    async getDetailsPurchaseById(id) {
        return await this.api.get(`${URL_PURCHASES}${id}/details/`);
    }
}

export const purchaseService = new PurchaseService();
