/**
 * ========================================
 * TEST FILE - PromotionService
 * ========================================
 */

import { authService, promotionService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create Promotion',
        method: 'POST',
        endpoint: '/v1/promotions/',
        execute: async (context) => {
            const result = await promotionService.create(PAYLOADS.promotion);
            if (result.success && result.data?.id) context.createdPromotionId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Promotions',
        method: 'GET',
        endpoint: '/v1/promotions/',
        execute: async () => await promotionService.getAllPromotions()
    },
    {
        name: 'GET Promotion By ID',
        method: 'GET',
        endpoint: '/v1/promotions/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPromotionId) throw new Error('No ID available');
            return await promotionService.getPromootionById(context.createdPromotionId);
        }
    },
    {
        name: 'GET Active Promotions',
        method: 'GET',
        endpoint: '/v1/promotions/active/',
        execute: async () => await promotionService.getActivePromotions()
    },
    {
        name: 'GET Inactive Promotions',
        method: 'GET',
        endpoint: '/v1/promotions/inactive/',
        execute: async () => await promotionService.getInactivePromotions()
    },
    {
        name: 'Update Promotion',
        method: 'PATCH',
        endpoint: '/v1/promotions/{id}/',
        needsId: true,
        execute: async (context) => {
             if (!context.createdPromotionId) throw new Error('No ID available');
             return await promotionService.update(context.createdPromotionId, PAYLOADS.promotionUpdate);
        }
    },
    {
        name: 'Deactivate Promotion',
        method: 'PATCH',
        endpoint: '/v1/promotions/{id}/deactivate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPromotionId) throw new Error('No ID available');
            return await promotionService.deactivate(context.createdPromotionId);
        }
    },
    {
        name: 'Activate Promotion',
        method: 'PATCH',
        endpoint: '/v1/promotions/{id}/activate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPromotionId) throw new Error('No ID available');
            return await promotionService.activate(context.createdPromotionId);
        }
    },
    {
        name: 'Delete Promotion',
        method: 'DELETE',
        endpoint: '/v1/promotions/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdPromotionId) throw new Error('No ID available');
            return await promotionService.delete(context.createdPromotionId);
        }
    }
];

export async function runTests() {
    console.log("=== PromotionService Tests ===\n");
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
    console.log("\n=== PromotionService Tests Complete ===");
}
