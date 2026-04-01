import { authService } from "./AuthService.js";
import {
    URL_REPORTS_PURCHASES,
    URL_REPORTS_PURCHASES_BY_SUPPLIER,
    URL_REPORTS_PURCHASES_BY_PERIOD
} from "../util/const.js";

class ReportPurchaseService {
    get api() {
        return authService.getApiClient();
    }

    async getReportsPurchases() {
        return this.api.get(URL_REPORTS_PURCHASES);
    }

    async getReportsPurchasesBySupplier() {
        return this.api.get(URL_REPORTS_PURCHASES_BY_SUPPLIER);
    }

    async getReportsPurchasesByPeriod() {
        return this.api.get(URL_REPORTS_PURCHASES_BY_PERIOD);
    }
}

export const reportPurchaseService = new ReportPurchaseService();
