/**
 * ========================================
 * TEST FILE - SaleService
 * ========================================
 */

import { authService, saleService, customerService, productService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create Sale',
        method: 'POST',
        endpoint: '/v1/sales/',
        execute: async (context) => {
            let custId = null;
            const custs = await customerService.getAllCustomers();
            if (custs.success && custs.data?.length > 0) {
                custId = custs.data[0].id;
            } else {
                const newCust = await customerService.create({ first_name: 'Auto', last_name: 'Customer', email: 'c' + Date.now() + '@t.com', number_phone: '123', address: 'NA' });
                if (newCust.success) custId = newCust.data.id;
            }

            let prodId = 1;
            const prods = await productService.getAllProducts();
            if (prods.success && prods.data?.length > 0) {
                prodId = prods.data[0].id;
            } else {
                const newProd = await productService.create({ category_id: 1, name: 'AutoProd', unique_code: 'P' + Date.now(), sale_price: 100, purchase_price: 80 });
                if (newProd.success) prodId = newProd.data.id;
            }

            const payload = JSON.parse(JSON.stringify(PAYLOADS.sale));
            payload.customer_id = custId;
            if (payload.details && payload.details.length > 0) {
                payload.details[0].product_id = prodId;
            }

            const result = await saleService.create(payload);
            if (result.success && result.data?.id) context.createdSaleId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Sales',
        method: 'GET',
        endpoint: '/v1/sales/',
        execute: async () => await saleService.getAllSales()
    },
    {
        name: 'GET Sale By ID',
        method: 'GET',
        endpoint: '/v1/sales/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSaleId) throw new Error('No ID available');
            return await saleService.getSaleById(context.createdSaleId);
        }
    },
    {
        name: 'GET Completed Sales',
        method: 'GET',
        endpoint: '/v1/sales/completed/',
        execute: async () => await saleService.getCompletedSales()
    },
    {
        name: 'GET Canceled Sales',
        method: 'GET',
        endpoint: '/v1/sales/canceled/',
        execute: async () => await saleService.getCanceledSales()
    },
    {
        name: 'GET Sale Details',
        method: 'GET',
        endpoint: '/v1/sales/{id}/details/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSaleId) throw new Error('No ID available');
            return await saleService.getDetailsSaleById(context.createdSaleId);
        }
    },
    {
        name: 'GET Sale Detail',
        method: 'GET',
        endpoint: '/v1/sales/{id}/details/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSaleId) throw new Error('No Sale ID available');

            const details = await saleService.getDetailsSaleById(context.createdSaleId);

            if (!details.success || !details.data || details.data.length === 0) {
                throw new Error('This sale has no details to query');
            }

            const detailId = details.data[0].id;

            return await saleService.getDetailSaleById(context.createdSaleId, detailId);
        }
    },
    {
        name: 'Update Sale',
        method: 'PATCH',
        endpoint: '/v1/sales/{id}/',
        needsId: true,
        execute: async (context) => {
             if (!context.createdSaleId) throw new Error('No ID available');
             return await saleService.update(context.createdSaleId, PAYLOADS.saleUpdate);
        }
    },
    {
        name: 'Cancel Sale',
        method: 'PATCH',
        endpoint: '/v1/sales/{id}/cancel/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSaleId) throw new Error('No ID available');
            return await saleService.cancel(context.createdSaleId);
        }
    },
    {
        name: 'Delete Sale',
        method: 'DELETE',
        endpoint: '/v1/sales/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSaleId) throw new Error('No ID available');
            return await saleService.delete(context.createdSaleId);
        }
    }
];

export async function runTests() {
    console.log("=== SaleService Tests ===\n");
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
    console.log("\n=== SaleService Tests Complete ===");
}
