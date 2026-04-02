/**
 * ========================================
 * TEST FILE - SupplierService
 * ========================================
 */

import { authService, supplierService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create Supplier',
        method: 'POST',
        endpoint: '/v1/suppliers/',
        execute: async (context) => {
            const result = await supplierService.create(PAYLOADS.supplier);
            if (result.success && result.data?.id) context.createdSupplierId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Suppliers',
        method: 'GET',
        endpoint: '/v1/suppliers/',
        execute: async () => await supplierService.getAllSuppliers()
    },
    {
        name: 'GET Supplier By ID',
        method: 'GET',
        endpoint: '/v1/suppliers/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSupplierId) throw new Error('No ID available');
            return await supplierService.getSupplierById(context.createdSupplierId);
        }
    },
    {
        name: 'GET Active Suppliers',
        method: 'GET',
        endpoint: '/v1/suppliers/active/',
        execute: async () => await supplierService.getActiveSuppliers()
    },
    {
        name: 'GET Inactive Suppliers',
        method: 'GET',
        endpoint: '/v1/suppliers/inactive/',
        execute: async () => await supplierService.getInactiveSuppliers()
    },
    {
        name: 'Update Supplier',
        method: 'PATCH',
        endpoint: '/v1/suppliers/{id}/',
        needsId: true,
        execute: async (context) => {
             if (!context.createdSupplierId) throw new Error('No ID available');
             return await supplierService.update(context.createdSupplierId, PAYLOADS.supplierUpdate);
        }
    },
    {
        name: 'Deactivate Supplier',
        method: 'PATCH',
        endpoint: '/v1/suppliers/{id}/deactivate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSupplierId) throw new Error('No ID available');
            return await supplierService.deactivate(context.createdSupplierId);
        }
    },
    {
        name: 'Activate Supplier',
        method: 'PATCH',
        endpoint: '/v1/suppliers/{id}/activate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSupplierId) throw new Error('No ID available');
            return await supplierService.activate(context.createdSupplierId);
        }
    },
    {
        name: 'Delete Supplier',
        method: 'DELETE',
        endpoint: '/v1/suppliers/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdSupplierId) throw new Error('No ID available');
            return await supplierService.delete(context.createdSupplierId);
        }
    }
];

export async function runTests() {
    console.log("=== SupplierService Tests ===\n");
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
    console.log("\n=== SupplierService Tests Complete ===");
}
