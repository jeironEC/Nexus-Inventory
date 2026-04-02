/**
 * ========================================
 * TEST FILE - CategoryService
 * ========================================
 */

import { authService, categoryService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create Category',
        method: 'POST',
        endpoint: '/v1/categories/',
        execute: async (context) => {
            const result = await categoryService.create(PAYLOADS.category);
            if (result.success && result.data?.id) context.createdCategoryId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Categories',
        method: 'GET',
        endpoint: '/v1/categories/',
        execute: async () => await categoryService.getAllCategories()
    },
    {
        name: 'GET Category By ID',
        method: 'GET',
        endpoint: '/v1/categories/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCategoryId) throw new Error('No ID available');
            return await categoryService.getCategoryById(context.createdCategoryId);
        }
    },
    {
        name: 'GET Active Categories',
        method: 'GET',
        endpoint: '/v1/categories/active/',
        execute: async () => await categoryService.getActiveCategories()
    },
    {
        name: 'GET Inactive Categories',
        method: 'GET',
        endpoint: '/v1/categories/inactive/',
        execute: async () => await categoryService.getInactiveCategories()
    },
    {
        name: 'Update Category',
        method: 'PATCH',
        endpoint: '/v1/categories/{id}/',
        needsId: true,
        execute: async (context) => {
             if (!context.createdCategoryId) throw new Error('No ID available');
             return await categoryService.update(context.createdCategoryId, PAYLOADS.categoryUpdate);
        }
    },
    {
        name: 'Deactivate Category',
        method: 'PATCH',
        endpoint: '/v1/categories/{id}/deactivate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCategoryId) throw new Error('No ID available');
            return await categoryService.deactivate(context.createdCategoryId);
        }
    },
    {
        name: 'Activate Category',
        method: 'PATCH',
        endpoint: '/v1/categories/{id}/activate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCategoryId) throw new Error('No ID available');
            return await categoryService.activate(context.createdCategoryId);
        }
    },
    {
        name: 'Delete Category',
        method: 'DELETE',
        endpoint: '/v1/categories/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCategoryId) throw new Error('No ID available');
            return await categoryService.delete(context.createdCategoryId);
        }
    }
];

export async function runTests() {
    console.log("=== CategoryService Tests ===\n");
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
    console.log("\n=== CategoryService Tests Complete ===");
}
