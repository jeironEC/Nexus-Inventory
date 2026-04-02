/**
 * ========================================
 * TEST FILE - InventoryMovementService
 * ========================================
 */

import { authService, inventoryMovementService } from "../services/index.js";

export const tests = [
    {
        name: 'GET All Movements',
        method: 'GET',
        endpoint: '/v1/inventory-movements/',
        execute: async () => await inventoryMovementService.getAllInventoryMovements()
    },
    {
        name: 'GET Movement By ID',
        method: 'GET',
        endpoint: '/v1/inventory-movements/{id}/',
        execute: async () => await inventoryMovementService.getInventoryMovementById(1)
    }
];

export async function runTests() {
    console.log("=== InventoryMovementService Tests ===\n");
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
    console.log("\n=== InventoryMovementService Tests Complete ===");
}
