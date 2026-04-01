import { authService } from "./AuthService.js";
import {
    URL_REPORTS_CUSTOMERS_PROMOTIONS,
    URL_REPORTS_CUSTOMERS_TOP
} from "../util/const.js";

class ReportCustomerService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getReportsCustomersPromotion() {
        return this.api.get(URL_REPORTS_CUSTOMERS_PROMOTIONS);
    }

    async getReportsCustomersTop() {
        return this.api.get(URL_REPORTS_CUSTOMERS_TOP);
    }
}

export const reportCustomerService = new ReportCustomerService();
