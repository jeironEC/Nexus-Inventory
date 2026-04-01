import { authService } from "./AuthService.js";
import {
    URL_REPORTS_PRODUCTS_BY_CATEGORY,
    URL_REPORTS_PRODUCTS_LOW_SELLING,
    URL_REPORTS_PRODUCTS_MOST_PURCHASED,
    URL_REPORTS_PRODUCTS_TOP_SELLING
} from "../util/const.js";

class ReportProductService {
    constructor() {
        this.api = authService.getApiClient();
    }

    async getReportsProductsByCategory() {
        return await this.api.get(URL_REPORTS_PRODUCTS_BY_CATEGORY);
    }

    async getReportsProductsLowSelling() {
        return await this.api.get(URL_REPORTS_PRODUCTS_LOW_SELLING);
    }

    async getReportsProductsMostPurchased() {
        return await this.api.get(URL_REPORTS_PRODUCTS_MOST_PURCHASED);
    }

    async getReportsProductsTopSelling() {
        return await this.api.get(URL_REPORTS_PRODUCTS_TOP_SELLING);
    }
}

export const reportProductService = new ReportProductService();
