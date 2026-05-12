// Proveedor para instanciar servicios de forma dinámica

import { BaseService } from './BaseService.js';
import * as URLs from '../utils/const.js';
import { saleService } from './SaleService.js';
import { purchaseService } from './PurchaseService.js';
import { invoiceService } from './InvoiceService.js';
import { inventoryService } from './InventoryService.js';
import { inventoryMovementService } from './InventoryMovementService.js';
import { saleReturnService } from './SaleReturnService.js';
import { purchaseReturnService } from './PurchaseReturnService.js';
import { reportService } from './ReportService.js';

class ServiceProvider {
    constructor() {
        this.services = {};
    }

    // Atajos para servicios comunes
    get categories() { return this.getService(URLs.URL_CATEGORIES); }
    get companies() { return this.getService(URLs.URL_COMPANIES); }
    get customers() { return this.getService(URLs.URL_CUSTOMERS); }
    get inventories() { return inventoryService; }
    get inventoryMovements() { return inventoryMovementService; }
    get invoices() { return invoiceService; }
    get products() { return this.getService(URLs.URL_PRODUCTS); }
    get purchaseReturns() { return purchaseReturnService; }
    get purchases() { return purchaseService; }
    get reports() { return reportService; }
    get roles() { return this.getService(URLs.URL_ROLES); }
    get saleReturns() { return saleReturnService; }
    get sales() { return saleService; }
    get suppliers() { return this.getService(URLs.URL_SUPPLIERS); }
    get users() { return this.getService(URLs.URL_USERS); }

    // Obtiene una instancia de BaseService para la URL proporcionada
    getService(url) {
        if (!this.services[url]) {
            this.services[url] = new BaseService(url);
        }
        return this.services[url];
    }
}

export const serviceProvider = new ServiceProvider();
