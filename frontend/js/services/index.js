/**
 * ========================================
 * ÍNDICE DE SERVICIOS
 * ========================================
 * Exporta todos los servicios del sistema
 * ========================================
 */

// Auth
export { authService } from './AuthService.js';

// Users
export { userService } from './UserService.js';

// Roles
export { roleService } from './RoleService.js';

// Categories
export { categoryService } from './CategoryService.js';

// Products
export { productService } from './ProductService.js';

// Customers
export { customerService } from './CustomerService.js';

// Promotions
export { promotionService } from './PromotionService.js';

// Customer Promotions
export { customerPromotionService } from './CustomerPromotionService.js';

// Inventories
export { inventoryService } from './InventoryService.js';

// Inventory Movements
export { inventoryMovementService } from './InventoryMovementService.js';

// Sales
export { saleService } from './SaleService.js';

// Sale Returns
export { saleReturnService } from './SaleReturnService.js';

// Purchases
export { purchaseService } from './PurchaseService.js';

// Purchase Returns
export { purchaseReturnService } from './PurchaseReturnService.js';

// Invoices
export { invoiceService } from './InvoiceService.js';

// Suppliers
export { supplierService } from './SupplierService.js';

// Reports - Sales
export { reportSaleService } from './ReportSaleService.js';

// Reports - Purchases
export { reportPurchaseService } from './ReportPurchaseService.js';

// Reports - Inventory
export { reportInventoryService } from './ReportInventoryService.js';

// Reports - Products
export { reportProductService } from './ReportProductService.js';

// Reports - Customers
export { reportCustomerService } from './ReportCustomerService.js';

// Reports - Invoices
export { reportInvoiceService } from './ReportInvoiceService.js';
