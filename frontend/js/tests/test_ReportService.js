/**
 * ========================================
 * TEST FILE - Report Services
 * ========================================
 */

import {
    authService,
    reportSaleService,
    reportPurchaseService,
    reportInventoryService,
    reportProductService,
    reportCustomerService,
    reportInvoiceService,
    reportSaleReturnService,
    reportPurchaseReturnService
} from "../services/index.js";

export const tests = [
    // --- REPORTS: SALES ---
    {
        name: 'Sales Report',
        method: 'GET',
        endpoint: '/v1/reports/sales/',
        execute: async () => await reportSaleService.getReportsSales()
    },
    {
        name: 'Sales By Customer',
        method: 'GET',
        endpoint: '/v1/reports/sales/by-customer/',
        execute: async () => await reportSaleService.getReportsSalesByCustomer()
    },
    {
        name: 'Sales By Payment Method',
        method: 'GET',
        endpoint: '/v1/reports/sales/by-payment-method/',
        execute: async () => await reportSaleService.getReportsSalesByPaymentMethod()
    },
    {
        name: 'Sales By Period',
        method: 'GET',
        endpoint: '/v1/reports/sales/by-period/',
        execute: async () => await reportSaleService.getReportsSalesByPeriod()
    },
    // --- REPORTS: PURCHASES ---
    {
        name: 'Purchases Report',
        method: 'GET',
        endpoint: '/v1/reports/purchases/',
        execute: async () => await reportPurchaseService.getReportsPurchases()
    },
    {
        name: 'Purchases By Supplier',
        method: 'GET',
        endpoint: '/v1/reports/purchases/by-supplier/',
        execute: async () => await reportPurchaseService.getReportsPurchasesBySupplier()
    },
    {
        name: 'Purchases By Period',
        method: 'GET',
        endpoint: '/v1/reports/purchases/by-period/',
        execute: async () => await reportPurchaseService.getReportsPurchasesByPeriod()
    },
    // --- REPORTS: INVENTORY ---
    {
        name: 'Inventory Report',
        method: 'GET',
        endpoint: '/v1/reports/inventory/',
        execute: async () => await reportInventoryService.getReportsInventories()
    },
    {
        name: 'Low Stock Report',
        method: 'GET',
        endpoint: '/v1/reports/inventory/low-stock/',
        execute: async () => await reportInventoryService.getReportsInventoriesLowStock()
    },
    {
        name: 'Inventory Movements Report',
        method: 'GET',
        endpoint: '/v1/reports/inventory/movements/',
        execute: async () => await reportInventoryService.getReportsInventoriesMovements()
    },
    // --- REPORTS: PRODUCTS ---
    {
        name: 'Top Selling Products',
        method: 'GET',
        endpoint: '/v1/reports/products/top-selling/',
        execute: async () => await reportProductService.getReportsProductsTopSelling()
    },
    {
        name: 'Low Selling Products',
        method: 'GET',
        endpoint: '/v1/reports/products/low-selling/',
        execute: async () => await reportProductService.getReportsProductsLowSelling()
    },
    {
        name: 'Most Purchased Products',
        method: 'GET',
        endpoint: '/v1/reports/products/most-purchased/',
        execute: async () => await reportProductService.getReportsProductsMostPurchased()
    },
    {
        name: 'Products By Category',
        method: 'GET',
        endpoint: '/v1/reports/products/by-category/',
        execute: async () => await reportProductService.getReportsProductsByCategory()
    },
    // --- REPORTS: CUSTOMERS ---
    {
        name: 'Top Customers',
        method: 'GET',
        endpoint: '/v1/reports/customers/top/',
        execute: async () => await reportCustomerService.getReportsCustomersTop()
    },
    {
        name: 'Customer Promotions Report',
        method: 'GET',
        endpoint: '/v1/reports/customers/promotions/',
        execute: async () => await reportCustomerService.getReportsCustomersPromotion()
    },
    // --- REPORTS: INVOICES ---
    {
        name: 'Invoices Report',
        method: 'GET',
        endpoint: '/v1/reports/invoices/',
        execute: async () => await reportInvoiceService.getReportsInvoices()
    },
    {
        name: 'Sales Invoices Report',
        method: 'GET',
        endpoint: '/v1/reports/invoices/sales/',
        execute: async () => await reportInvoiceService.getReportsInvoicesSales()
    },
    {
        name: 'Purchases Invoices Report',
        method: 'GET',
        endpoint: '/v1/reports/invoices/purchases/',
        execute: async () => await reportInvoiceService.getReportsInvoicesPurchases()
    },
    // --- REPORTS: RETURNS ---
    {
        name: 'Sale Returns Report',
        method: 'GET',
        endpoint: '/v1/reports/sale-returns/',
        execute: async () => await reportSaleReturnService.getReportsSaleReturns()
    },
    {
        name: 'Purchase Returns Report',
        method: 'GET',
        endpoint: '/v1/reports/purchase-returns/',
        execute: async () => await reportPurchaseReturnService.getReportsPurchaseReturns()
    }
];


export async function runTests() {
    console.log("=== Report Services Tests ===\n");
    if (!authService.isAuthenticated()) await authService.login("jeiron@gmail.com", "jeiron123");

    const context = {};
    for (const test of tests) {
        console.log(`Test: ${test.method} ${test.endpoint}`);
        try {
            const result = await test.execute(context);
            if (!result || !result.success) throw new Error(result?.message || 'Operation failed');
            console.log(`  ✓ ${test.name}: PASS`);
        } catch (e) {
            console.log(`  ✗ ${test.name}: FAIL -`, e.message);
        }
    }
    console.log("\n=== Report Services Tests Complete ===");
}
