/**
 * ========================================
 * TEST FILE - InvoiceService
 * ========================================
 */

import { authService, invoiceService } from "../services/index.js";

export const tests = [
    {
        name: 'GET All Invoices',
        method: 'GET',
        endpoint: '/v1/invoices/',
        execute: async () => await invoiceService.getAllInvoices()
    },
    {
        name: 'GET Invoice By ID',
        method: 'GET',
        endpoint: '/v1/invoices/{id}/',
        execute: async () => await invoiceService.getInvoiceById(1)
    },
    {
        name: 'Cancel Invoice',
        method: 'PATCH',
        endpoint: '/v1/invoices/{id}/cancel/',
        execute: async () => await invoiceService.cancel(1)
    }
];

export async function runTests() {
    console.log("=== InvoiceService Tests ===\n");
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
    console.log("\n=== InvoiceService Tests Complete ===");
}
