/**
 * ========================================
 * TEST FILE - PurchaseService
 * ========================================
 */

import { authService, purchaseService, supplierService, productService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create Purchase',
        method: 'POST',
        endpoint: '/v1/purchases/',
        execute: async (context) => {
            let suppId = 1;
            const supps = await supplierService.getAllSuppliers();
            if (supps.success && supps.data?.length > 0) {
                suppId = supps.data[0].id;
            } else {
                const newSupp = await supplierService.create({ name: 'AutoSupplier', email: 's' + Date.now() + '@t.com', number_phone: '123', address: 'NA' });
                if (newSupp.success) suppId = newSupp.data.id;
            }

            let prodId = 1;
            const prods = await productService.getAllProducts();
            if (prods.success && prods.data?.length > 0) {
                prodId = prods.data[0].id;
            } else {
                const newProd = await productService.create({ category_id: 1, name: 'AutoProd', unique_code: 'P' + Date.now(), sale_price: 100, purchase_price: 80 });
                if (newProd.success) prodId = newProd.data.id;
            }

            const payload = JSON.parse(JSON.stringify(PAYLOADS.purchase));
            payload.supplier_id = suppId;
            if (payload.details && payload.details.length > 0) {
                payload.details[0].product_id = prodId;
            }

            const result = await purchaseService.create(payload);
            if (result.success && result.data?.id) context.createdPurchaseId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Purchases',
        method: 'GET',
        endpoint: '/v1/purchases/',
        execute: async () => await purchaseService.getAllPurchases()
    },
    {
        name: 'GET Purchase By ID',
        method: 'GET',
        endpoint: '/v1/purchases/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPurchaseId) throw new Error('No ID available');
            return await purchaseService.getPurchaseById(context.createdPurchaseId);
        }
    },
    {
        name: 'GET Completed Purchases',
        method: 'GET',
        endpoint: '/v1/purchases/completed/',
        execute: async () => await purchaseService.getCompletedPurchases()
    },
    {
        name: 'GET Canceled Purchases',
        method: 'GET',
        endpoint: '/v1/purchases/canceled/',
        execute: async () => await purchaseService.getCanceledPurchases()
    },
    {
        name: 'GET Purchase Details',
        method: 'GET',
        endpoint: '/v1/purchases/{id}/details/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPurchaseId) throw new Error('No ID available');
            return await purchaseService.getDetailsPurchaseById(context.createdPurchaseId);
        }
    },
    {
            name: 'GET Purchase Detail',
            method: 'GET',
            endpoint: '/v1/purchases/{id}/details/{id}/',
            needsId: true,
            execute: async (context) => {
                if (!context.createdPurchaseId) throw new Error('No Sale ID available');

                const details = await purchaseService.getDetailsPurchaseById(context.createdPurchaseId);

                if (!details.success || !details.data || details.data.length === 0) {
                    throw new Error('This sale has no details to query');
                }

                const detailId = details.data[0].id;

                return await purchaseService.getDetailPurchaseById(context.createdPurchaseId, detailId);
            }
        },
    {
        name: 'Update Purchase',
        method: 'PATCH',
        endpoint: '/v1/purchases/{id}/',
        needsId: true,
        execute: async (context) => {
             if (!context.createdPurchaseId) throw new Error('No ID available');
             return await purchaseService.update(context.createdPurchaseId, PAYLOADS.purchaseUpdate);
        }
    },
    {
        name: 'Cancel Purchase',
        method: 'PATCH',
        endpoint: '/v1/purchases/{id}/cancel/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPurchaseId) throw new Error('No ID available');
            return await purchaseService.cancel(context.createdPurchaseId);
        }
    },
    {
        name: 'Delete Purchase',
        method: 'DELETE',
        endpoint: '/v1/purchases/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPurchaseId) throw new Error('No ID available');
            return await purchaseService.delete(context.createdPurchaseId);
        }
    }
];

export async function runTests() {
    console.log("=== PurchaseService Tests ===\n");
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
    console.log("\n=== PurchaseService Tests Complete ===");
}
