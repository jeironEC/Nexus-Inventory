// Servicio para gestionar devoluciones de ventas

import { BaseService } from "./BaseService.js";
import { URL_SALE_RETURNS } from "../utils/const.js";

class SaleReturnService extends BaseService {
    constructor() {
        super(URL_SALE_RETURNS);
    }

    // Cancela una devolución de venta
    async cancel(id) {
        return await this.api.patch(`${URL_SALE_RETURNS}${id}/cancel/`);
    }

    async getDetailsSaleReturnById(id) {
        return await this.api.get(`${URL_SALE_RETURNS}${id}/details/`);
    }
}

export const saleReturnService = new SaleReturnService();
