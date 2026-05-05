// Servicio para gestionar facturas

import { BaseService } from "./BaseService.js";
import { URL_INVOICES } from "../utils/const.js";

class InvoiceService extends BaseService {
    constructor() {
        super(URL_INVOICES);
    }

    // Cancela una factura
    async cancel(id) {
        return await this.api.patch(`${URL_INVOICES}${id}/cancel/`);
    }

    // Descarga el PDF de una factura
    async downloadPdf(id) {
        return await this.api.get(`${URL_INVOICES}${id}/pdf/`, { responseType: 'blob' });
    }
}

export const invoiceService = new InvoiceService();
