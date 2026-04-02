/**
 * ========================================
 * TEST FILE - InventoryService
 * ========================================
 */

import { authService, inventoryService } from "../services/index.js";

export const tests = [
    {
        name: 'GET All Inventories',
        method: 'GET',
        endpoint: '/v1/inventories/',
        execute: async () => await inventoryService.getAllInventories()
    },
    {
        name: 'GET Low Stock',
        method: 'GET',
        endpoint: '/v1/inventories/low-stock/',
        execute: async () => await inventoryService.getLowInventory()
    },
    {
        name: 'GET Inventory By Product',
        method: 'GET',
        endpoint: '/v1/inventories/product/{id}/',
        execute: async () => await inventoryService.getProductInventory(1)
    }
];

export async function runTests() {
    console.log("=== InventoryService Tests ===\n");
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
    console.log("\n=== InventoryService Tests Complete ===");
}
