/**
 * ========================================
 * TEST FILE - SaleReturnService
 * ========================================
 */

import { authService, saleReturnService, saleService, productService, categoryService, customerService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create Sale Return',
        method: 'POST',
        endpoint: '/v1/sale-returns/',
        execute: async (context) => {
            let custId = null;
            const custs = await customerService.getAllCustomers();
            if (custs.success && custs.data?.length > 0) custId = custs.data[0].id;
            else {
                const newCust = await customerService.create({ first_name: 'Auto', last_name: 'Customer', email: 'c' + Date.now() + '@t.com', number_phone: '123', address: 'NA' });
                if (newCust.success) custId = newCust.data.id;
            }

            let catId = 1;
            const cats = await categoryService.getAllCategories();
            if (cats.success && cats.data?.length > 0) catId = cats.data[0].id;
            else {
                const newCat = await categoryService.create({ name: 'AutoCat', description: 'Dep' });
                if (newCat.success) catId = newCat.data.id;
            }

            let prodId = 1;
            const newProd = await productService.create({ category_id: catId, name: 'AutoProdNew', unique_code: 'PN'+Date.now(), sale_price: 150, purchase_price: 100 });
            if (newProd.success) prodId = newProd.data.id;

            let saleId = 1;
            const newSale = await saleService.create({
                customer_id: custId,
                payment_method: "CASH",
                details: [{ product_id: prodId, quantity: 2, unit_price: "50.00" }]
            });
            if (newSale.success) saleId = newSale.data.id;

            const payload = JSON.parse(JSON.stringify(PAYLOADS.saleReturn));
            payload.sale_id = saleId;
            if (payload.details && payload.details.length > 0) {
                payload.details[0].product_id = prodId;
            }

            const result = await saleReturnService.create(payload);
            if (result.success && result.data?.id) context.createdSaleReturnId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Sale Returns',
        method: 'GET',
        endpoint: '/v1/sale-returns/',
        execute: async () => await saleReturnService.getAllSaleReturns()
    },
    {
        name: 'GET Sale Return By ID',
        method: 'GET',
        endpoint: '/v1/sale-returns/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSaleReturnId) throw new Error('No ID available');
            return await saleReturnService.getSaleReturnById(context.createdSaleReturnId);
        }
    },
    {
        name: 'GET Completed Sale Returns',
        method: 'GET',
        endpoint: '/v1/sale-returns/completed/',
        execute: async () => await saleReturnService.getCompletedSaleReturns()
    },
    {
        name: 'GET Canceled Sale Returns',
        method: 'GET',
        endpoint: '/v1/sale-returns/canceled/',
        execute: async () => await saleReturnService.getCanceledSaleReturns()
    },
    {
        name: 'GET Sale Return Details',
        method: 'GET',
        endpoint: '/v1/sale-returns/{id}/details/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSaleReturnId) throw new Error('No ID available');
            return await saleReturnService.getDetailsSaleReturnById(context.createdSaleReturnId);
        }
    },
    {
        name: 'GET Sale Return Detail',
        method: 'GET',
        endpoint: '/v1/sale-returns/{id}/details/{detail_id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSaleReturnId) throw new Error('No ID available');
            const details = await saleReturnService.getDetailsSaleReturnById(context.createdSaleReturnId);
            if (details.success && details.data?.length > 0) {
                return await saleReturnService.getDetailSaleReturnById(context.createdSaleReturnId, details.data[0].id);
            }
            throw new Error('No Details found for this Return');
        }
    },
    {
        name: 'Update Sale Return',
        method: 'PATCH',
        endpoint: '/v1/sale-returns/{id}/',
        needsId: true,
        execute: async (context) => {
             if (!context.createdSaleReturnId) throw new Error('No ID available');
             return await saleReturnService.update(context.createdSaleReturnId, { reason: "Updated reason" });
        }
    },
    {
        name: 'Cancel Sale Return',
        method: 'PATCH',
        endpoint: '/v1/sale-returns/{id}/cancel/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSaleReturnId) throw new Error('No ID available');
            return await saleReturnService.cancel(context.createdSaleReturnId);
        }
    },
    {
        name: 'Delete Sale Return',
        method: 'DELETE',
        endpoint: '/v1/sale-returns/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSaleReturnId) throw new Error('No ID available');
            return await saleReturnService.delete(context.createdSaleReturnId);
        }
    }
];

export async function runTests() {
    console.log("=== SaleReturnService Tests ===\n");
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
    console.log("\n=== SaleReturnService Tests Complete ===");
}
