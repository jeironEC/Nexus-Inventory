import { authService } from "./AuthService.js";
import {
    URL_REPORTS_INVENTORIES,
    URL_REPORTS_INVENTORIES_LOW_STOCK,
    URL_REPORTS_INVENTORIES_MOVEMENTS,
} from "../util/const.js";


class ReportInventoryService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getReportsInventories() {
        return await this.api.get(URL_REPORTS_INVENTORIES);
    }

    async getReportsInventoriesLowStock() {
        return await this.api.get(URL_REPORTS_INVENTORIES_LOW_STOCK);
    }

    async getReportsInventoriesMovements() {
        return await this.api.get(URL_REPORTS_INVENTORIES_MOVEMENTS);
    }
}

export const reportInventoryService = new ReportInventoryService();
