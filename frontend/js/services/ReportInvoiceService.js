import { authService } from "./AuthService.js";
import {
    URL_REPORTS_INVOICES,
    URL_REPORTS_INVOICES_SALES,
    URL_REPORTS_INVOICES_PURCHASES,
} from "../util/const.js";

class ReportInvoiceService {
    get api() {
        return authService.getApiClient();
    }

    async getReportsInvoices() {
        return await this.api.get(URL_REPORTS_INVOICES);
    }

    async getReportsInvoicesSales() {
        return await this.api.get(URL_REPORTS_INVOICES_SALES);
    }

    async getReportsInvoicesPurchases() {
        return await this.api.get(URL_REPORTS_INVOICES_PURCHASES);
    }
}

export const reportInvoiceService = new ReportInvoiceService();
