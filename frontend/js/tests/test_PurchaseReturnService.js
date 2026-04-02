/**
 * ========================================
 * TEST FILE - PurchaseReturnService
 * ========================================
 */

import { authService, purchaseReturnService, purchaseService, categoryService, productService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create Purchase Return',
        method: 'POST',
        endpoint: '/v1/purchase-returns/',
        execute: async (context) => {
            let catId = 1;
            const cats = await categoryService.getAllCategories();
            if (cats.success && cats.data?.length > 0) catId = cats.data[0].id;
            else {
                const newCat = await categoryService.create({ name: 'AutoCat', description: 'Dep' });
                if (newCat.success) catId = newCat.data.id;
            }

            let prodId = 1;
            const newProd = await productService.create({ category_id: catId, name: 'AutoProdNew2', unique_code: 'P'+Date.now(), sale_price: 150, purchase_price: 100 });
            if (newProd.success) prodId = newProd.data.id;

            let purchId = 1;
            const newPurch = await purchaseService.create({
                supplier_id: 1,
                details: [{ product_id: prodId, quantity: 2, unit_cost: "50.00" }]
            });
            if (newPurch.success) purchId = newPurch.data.id;

            const payload = JSON.parse(JSON.stringify(PAYLOADS.purchaseReturn));
            payload.purchase_id = purchId;
            if (payload.details && payload.details.length > 0) {
                payload.details[0].product_id = prodId;
            }

            const result = await purchaseReturnService.create(payload);
            if (result.success && result.data?.id) context.createdPurchaseReturnId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Purchase Returns',
        method: 'GET',
        endpoint: '/v1/purchase-returns/',
        execute: async () => await purchaseReturnService.getAllPurchaseReturns()
    },
    {
        name: 'GET Purchase Return By ID',
        method: 'GET',
        endpoint: '/v1/purchase-returns/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPurchaseReturnId) throw new Error('No ID available');
            return await purchaseReturnService.getPurchaseReturnById(context.createdPurchaseReturnId);
        }
    },
    {
        name: 'GET Completed Purchase Returns',
        method: 'GET',
        endpoint: '/v1/purchase-returns/completed/',
        execute: async () => await purchaseReturnService.getCompletedPurchaseReturns()
    },
    {
        name: 'GET Canceled Purchase Returns',
        method: 'GET',
        endpoint: '/v1/purchase-returns/canceled/',
        execute: async () => await purchaseReturnService.getCanceledPurchaseReturns()
    },
    {
        name: 'GET Purchase Return Details',
        method: 'GET',
        endpoint: '/v1/purchase-returns/{id}/details/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPurchaseReturnId) throw new Error('No ID available');
            return await purchaseReturnService.getDetailsPurchaseReturnById(context.createdPurchaseReturnId);
        }
    },
    {
        name: 'GET Purchase Return Detail',
        method: 'GET',
        endpoint: '/v1/purchase-returns/{id}/details/{detail_id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPurchaseReturnId) throw new Error('No ID available');
            const details = await purchaseReturnService.getDetailsPurchaseReturnById(context.createdPurchaseReturnId);
            if (details.success && details.data?.length > 0) {
                return await purchaseReturnService.getDetailPurchaseReturnById(context.createdPurchaseReturnId, details.data[0].id);
            }
            throw new Error('No Details found for this Return');
        }
    },
    {
        name: 'Update Purchase Return',
        method: 'PATCH',
        endpoint: '/v1/purchase-returns/{id}/',
        needsId: true,
        execute: async (context) => {
             if (!context.createdPurchaseReturnId) throw new Error('No ID available');
             return await purchaseReturnService.update(context.createdPurchaseReturnId, { reason: "Updated reason" });
        }
    },
    {
        name: 'Cancel Purchase Return',
        method: 'PATCH',
        endpoint: '/v1/purchase-returns/{id}/cancel/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPurchaseReturnId) throw new Error('No ID available');
            return await purchaseReturnService.cancel(context.createdPurchaseReturnId);
        }
    },
    {
        name: 'Delete Purchase Return',
        method: 'DELETE',
        endpoint: '/v1/purchase-returns/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPurchaseReturnId) throw new Error('No ID available');
            return await purchaseReturnService.delete(context.createdPurchaseReturnId);
        }
    }
];

export async function runTests() {
    console.log("=== PurchaseReturnService Tests ===\n");
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
    console.log("\n=== PurchaseReturnService Tests Complete ===");
}
