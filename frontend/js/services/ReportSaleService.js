import { authService } from "./AuthService.js";
import {
    URL_REPORTS_SALES,
    URL_REPORTS_SALES_BY_CUSTOMER,
    URL_REPORTS_SALES_BY_PAYMENT_METHOD,
    URL_REPORTS_SALES_BY_PERIOD
} from "../util/const.js";

class ReportSaleService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getReportsSales() {
        return this.api.get(URL_REPORTS_SALES);
    }

    async getReportsSalesByCustomer() {
        return this.api.get(URL_REPORTS_SALES_BY_CUSTOMER);
    }

    async getReportsSalesByPaymentMethod() {
        return this.api.get(URL_REPORTS_SALES_BY_PAYMENT_METHOD);
    }

    async getReportsSalesByPeriod() {
        return this.api.get(URL_REPORTS_SALES_BY_PERIOD);
    }
}

export const reportSaleService = new ReportSaleService();
