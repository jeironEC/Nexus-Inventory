/**
 * ========================================
 * TESTS INDEX
 * ========================================
 * Run all tests or individual ones
 * ========================================
 */

// Import all test functions
import { runTests as testUserService } from './test_UserService.js';
import { runTests as testRoleService } from './test_RoleService.js';
import { runTests as testCategoryService } from './test_CategoryService.js';
import { runTests as testProductService } from './test_ProductService.js';
import { runTests as testCustomerService } from './test_CustomerService.js';
import { runTests as testSupplierService } from './test_SupplierService.js';
import { runTests as testPromotionService } from './test_PromotionService.js';
import { runTests as testCustomerPromotionService } from './test_CustomerPromotionService.js';
import { runTests as testInventoryService } from './test_InventoryService.js';
import { runTests as testInventoryMovementService } from './test_InventoryMovementService.js';
import { runTests as testSaleService } from './test_SaleService.js';
import { runTests as testPurchaseService } from './test_PurchaseService.js';
import { runTests as testSaleReturnService } from './test_SaleReturnService.js';
import { runTests as testPurchaseReturnService } from './test_PurchaseReturnService.js';
import { runTests as testInvoiceService } from './test_InvoiceService.js';
import { runTests as testReportServices } from './test_ReportService.js';

/**
 * Run all tests sequentially
 */
async function runAllTests() {
    console.log("========================================");
    console.log("RUNNING ALL SERVICE TESTS");
    console.log("========================================\n");

    const tests = [
        { name: "UserService", fn: testUserService },
        { name: "RoleService", fn: testRoleService },
        { name: "CategoryService", fn: testCategoryService },
        { name: "ProductService", fn: testProductService },
        { name: "CustomerService", fn: testCustomerService },
        { name: "SupplierService", fn: testSupplierService },
        { name: "PromotionService", fn: testPromotionService },
        { name: "CustomerPromotionService", fn: testCustomerPromotionService },
        { name: "InventoryService", fn: testInventoryService },
        { name: "InventoryMovementService", fn: testInventoryMovementService },
        { name: "SaleService", fn: testSaleService },
        { name: "PurchaseService", fn: testPurchaseService },
        { name: "SaleReturnService", fn: testSaleReturnService },
        { name: "PurchaseReturnService", fn: testPurchaseReturnService },
        { name: "InvoiceService", fn: testInvoiceService },
        { name: "ReportServices", fn: testReportServices },
    ];

    for (const test of tests) {
        console.log(`\n${"=".repeat(50)}`);
        console.log(`RUNNING: ${test.name}`);
        console.log("=".repeat(50));
        try {
            await test.fn();
        } catch (e) {
            console.error(`!!! ${test.name} CRASHED !!!`, e.message);
        }
    }

    console.log("\n========================================");
    console.log("ALL TESTS COMPLETED");
    console.log("========================================");
}


runAllTests();
