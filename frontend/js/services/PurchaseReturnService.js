// Servicio para gestionar devoluciones de compras

import { BaseService } from "./BaseService.js";
import { URL_PURCHASE_RETURNS } from "../utils/const.js";

class PurchaseReturnService extends BaseService {
    constructor() {
        super(URL_PURCHASE_RETURNS);
    }

    // Cancela una devolución de compra
    async cancel(id) {
        return await this.api.patch(`${URL_PURCHASE_RETURNS}${id}/cancel/`);
    }
}

export const purchaseReturnService = new PurchaseReturnService();
