import { authService } from "./AuthService.js";
import {
    URL_REPORTS_SALE_RETURNS
} from "../util/const.js";

class ReportSaleReturnService {
    get api() {
        return authService.getApiClient();
    }

    async getReportsSaleReturns() {
        return this.api.get(URL_REPORTS_SALE_RETURNS);
    }
}

export const reportSaleReturnService = new ReportSaleReturnService();
