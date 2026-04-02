import { authService } from "./AuthService.js";
import {
    URL_REPORTS_PURCHASE_RETURNS
} from "../util/const.js";

class ReportPurchaseReturnService {
    get api() {
        return authService.getApiClient();
    }

    async getReportsPurchaseReturns() {
        return this.api.get(URL_REPORTS_PURCHASE_RETURNS);
    }
}

export const reportPurchaseReturnService = new ReportPurchaseReturnService();
