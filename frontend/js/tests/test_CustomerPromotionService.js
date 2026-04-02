/**
 * ========================================
 * TEST FILE - CustomerPromotionService
 * ========================================
 */

import { authService, customerPromotionService, customerService, promotionService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create Customer Promotion',
        method: 'POST',
        endpoint: '/v1/customer-promotions/',
        execute: async (context) => {
            let custId = 1;
            let promoId = 1;

            const custs = await customerService.getAllCustomers();
            if (custs.success && custs.data?.length > 0) custId = custs.data[0].id;

            const promos = await promotionService.getAllPromotions();
            if (promos.success && promos.data?.length > 0) promoId = promos.data[0].id;

            const payload = { ...PAYLOADS.customerPromotion, customer_id: custId, promotion_id: promoId };
            const result = await customerPromotionService.create(payload);
            if (result.success && result.data?.id) context.createdCustomerPromotionId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Customer Promotions',
        method: 'GET',
        endpoint: '/v1/customer-promotions/',
        execute: async () => await customerPromotionService.getAllCustomerPromotions()
    },
    {
        name: 'GET Customer Promotion By ID',
        method: 'GET',
        endpoint: '/v1/customer-promotions/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCustomerPromotionId) throw new Error('No ID available');
            return await customerPromotionService.getCustomerPromotionById(context.createdCustomerPromotionId);
        }
    },
    {
        name: 'Update Customer Promotion',
        method: 'PATCH',
        endpoint: '/v1/customer-promotions/{id}/',
        needsId: true,
        execute: async (context) => {
             if (!context.createdCustomerPromotionId) throw new Error('No ID available');
             return await customerPromotionService.update(context.createdCustomerPromotionId, { applied: true });
        }
    },
    {
        name: 'Apply Customer Promotion',
        method: 'PATCH',
        endpoint: '/v1/customer-promotions/{id}/apply/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCustomerPromotionId) throw new Error('No ID available');
            return await customerPromotionService.apply(context.createdCustomerPromotionId);
        }
    },
    {
        name: 'Delete Customer Promotion',
        method: 'DELETE',
        endpoint: '/v1/customer-promotions/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCustomerPromotionId) throw new Error('No ID available');
            return await customerPromotionService.delete(context.createdCustomerPromotionId);
        }
    }
];

export async function runTests() {
    console.log("=== CustomerPromotionService Tests ===\n");
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
    console.log("\n=== CustomerPromotionService Tests Complete ===");
}
