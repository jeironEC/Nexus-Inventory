// Servicio para gestionar ventas

import { BaseService } from "./BaseService.js";
import { URL_SALES } from "../utils/const.js";

class SaleService extends BaseService {
    constructor() {
        super(URL_SALES);
    }

    // Cancela una venta
    async cancel(id) {
        return await this.api.patch(`${URL_SALES}${id}/cancel/`);
    }

    // Obtiene los detalles de una venta por su ID
    async getDetailsSaleById(id) {
        return await this.api.get(`${URL_SALES}${id}/details/`);
    }
}

export const saleService = new SaleService();
