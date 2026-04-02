/**
 * ========================================
 * TEST FILE - ProductService
 * ========================================
 */

import { authService, productService, categoryService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create Product',
        method: 'POST',
        endpoint: '/v1/products/',
        execute: async (context) => {
            let catId = 1;
            const cats = await categoryService.getAllCategories();
            if (cats.success && cats.data?.length > 0) {
                catId = cats.data[0].id;
            } else {
                const newCat = await categoryService.create({ name: 'AutogenCat', description: 'Dependency' });
                if (newCat.success) catId = newCat.data.id;
            }
            const payload = { ...PAYLOADS.product, category_id: catId };
            const result = await productService.create(payload);
            if (result.success && result.data?.id) context.createdProductId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Products',
        method: 'GET',
        endpoint: '/v1/products/',
        execute: async () => await productService.getAllProducts()
    },
    {
        name: 'GET Product By ID',
        method: 'GET',
        endpoint: '/v1/products/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdProductId) throw new Error('No ID available');
            return await productService.getProductById(context.createdProductId);
        }
    },
    {
        name: 'GET Active Products',
        method: 'GET',
        endpoint: '/v1/products/active/',
        execute: async () => await productService.getActiveProducts()
    },
    {
        name: 'GET Inactive Products',
        method: 'GET',
        endpoint: '/v1/products/inactive/',
        execute: async () => await productService.getInactiveProducts()
    },
    {
        name: 'Update Product',
        method: 'PATCH',
        endpoint: '/v1/products/{id}/',
        needsId: true,
        execute: async (context) => {
             if (!context.createdProductId) throw new Error('No ID available');
             return await productService.update(context.createdProductId, PAYLOADS.productUpdate);
        }
    },
    {
        name: 'Deactivate Product',
        method: 'PATCH',
        endpoint: '/v1/products/{id}/deactivate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdProductId) throw new Error('No ID available');
            return await productService.deactivate(context.createdProductId);
        }
    },
    {
        name: 'Activate Product',
        method: 'PATCH',
        endpoint: '/v1/products/{id}/activate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdProductId) throw new Error('No ID available');
            return await productService.activate(context.createdProductId);
        }
    },
    {
        name: 'Delete Product',
        method: 'DELETE',
        endpoint: '/v1/products/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdProductId) throw new Error('No ID available');
            return await productService.delete(context.createdProductId);
        }
    }
];

export async function runTests() {
    console.log("=== ProductService Tests ===\n");
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
    console.log("\n=== ProductService Tests Complete ===");
}
