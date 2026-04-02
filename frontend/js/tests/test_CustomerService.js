/**
 * ========================================
 * TEST FILE - CustomerService
 * ========================================
 */

import { authService, customerService } from "../services/index.js";
import { PAYLOADS } from "./payloads.js";

export const tests = [
    {
        name: 'Create Customer',
        method: 'POST',
        endpoint: '/v1/customers/',
        execute: async (context) => {
            const result = await customerService.create(PAYLOADS.customer);
            if (result.success && result.data?.id) context.createdCustomerId = result.data.id;
            return result;
        }
    },
    {
        name: 'GET All Customers',
        method: 'GET',
        endpoint: '/v1/customers/',
        execute: async () => await customerService.getAllCustomers()
    },
    {
        name: 'GET Customer By ID',
        method: 'GET',
        endpoint: '/v1/customers/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCustomerId) throw new Error('No ID available');
            return await customerService.getCustomerById(context.createdCustomerId);
        }
    },
    {
        name: 'GET Active Customers',
        method: 'GET',
        endpoint: '/v1/customers/active/',
        execute: async () => await customerService.getActiveCustomers()
    },
    {
        name: 'GET Inactive Customers',
        method: 'GET',
        endpoint: '/v1/customers/inactive/',
        execute: async () => await customerService.getInactiveCustomers()
    },
    {
        name: 'GET Customer Promotions',
        method: 'GET',
        endpoint: '/v1/customers/{id}/list-promotions/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCustomerId) throw new Error('No ID available');
            return await customerService.getListPromotions(context.createdCustomerId);
        }
    },
    {
        name: 'Update Customer',
        method: 'PATCH',
        endpoint: '/v1/customers/{id}/',
        needsId: true,
        execute: async (context) => {
             if (!context.createdCustomerId) throw new Error('No ID available');
             return await customerService.update(context.createdCustomerId, PAYLOADS.customerUpdate);
        }
    },
    {
        name: 'Deactivate Customer',
        method: 'PATCH',
        endpoint: '/v1/customers/{id}/deactivate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCustomerId) throw new Error('No ID available');
            return await customerService.deactivate(context.createdCustomerId);
        }
    },
    {
        name: 'Activate Customer',
        method: 'PATCH',
        endpoint: '/v1/customers/{id}/activate/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCustomerId) throw new Error('No ID available');
            return await customerService.activate(context.createdCustomerId);
        }
    },
    {
        name: 'Delete Customer',
        method: 'DELETE',
        endpoint: '/v1/customers/{id}/',
        needsId: true,
        execute: async (context) => {
            if (!context.createdCustomerId) throw new Error('No ID available');
            return await customerService.delete(context.createdCustomerId);
        }
    }
];

export async function runTests() {
    console.log("=== CustomerService Tests ===\n");
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
    console.log("\n=== CustomerService Tests Complete ===");
}
