import { authService } from "./AuthService.js";
import {
    URL_INVOICES,
    URL_INVOICE_SALE,
    URL_INVOICE_PURCHASE,
} from "../util/const.js";

class InvoiceService {
    get api() {
        return authService.getApiClient();
    }

    async getAllInvoices(filtros = {}) {
        const params = new URLSearchParams(filtros).toString();
        const endpoint = params ? `${URL_INVOICES}?${params}` : `${URL_INVOICES}`;
        return await this.api.get(endpoint);
    }

    async getInvoiceById(id) {
        return await this.api.get(`${URL_INVOICES}${id}/`);
    }

    async cancel(id) {
        return await this.api.patch(`${URL_INVOICES}${id}/cancel/`);
    }

    async getInvoiceBySaleId(id) {
        return await this.api.get(`${URL_INVOICE_SALE}${id}/`);
    }

    async getInvoiceByPurchaseId(id) {
        return await this.api.get(`${URL_INVOICE_PURCHASE}${id}/`);
    }
}

export const invoiceService = new InvoiceService();
