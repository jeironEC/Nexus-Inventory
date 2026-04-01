export const DEFAULT_TIMEOUT = 3000;

// =========================================================================
// URLS ENDPOINTS
// =========================================================================

// URL BASE
export const URL_BASE = "http://127.0.0.1:8000";

// URLS TOKEN
export const URL_AUTH_TOKEN = "/v1/auth/token/";
export const URL_AUTH_REFRESH = `${URL_AUTH_TOKEN}refresh/`;

// URLS USERS
export const URL_USERS = "/v1/users/";
export const URL_ACTIVE_USERS = `${URL_USERS}active/`;
export const URL_INACTIVE_USERS = `${URL_USERS}inactive/`;
export const URL_USERS_PROFILE = `${URL_USERS}me/`;

// URLS ROLES
export const URL_ROLES = "/v1/roles/";
export const URL_ACTIVE_ROLES = `${URL_ROLES}active/`;
export const URL_INACTIVE_ROLES = `${URL_ROLES}inactive/`;

// URLS CATEGORIES
export const URL_CATEGORIES = "/v1/categories/";
export const URL_ACTIVE_CATEGORIES = `${URL_CATEGORIES}active/`;
export const URL_INACTIVE_CATEGORIES = `${URL_CATEGORIES}inactive/`;

// URLS PRODUCTS
export const URL_PRODUCTS = "/v1/products/";
export const URL_ACTIVE_PRODUCTS = `${URL_PRODUCTS}active/`;
export const URL_INACTIVE_PRODUCTS = `${URL_PRODUCTS}inactive/`;

// URLS INVENTORIES
export const URL_INVENTORIES = "/v1/inventories/";
export const URL_LOW_INVENTORIES = `${URL_INVENTORIES}low-stock/`;
export const URL_PRODUCT_INVENTORIES = `${URL_INVENTORIES}product/`;

// URLS INVENTORY MOVEMENTS
export const URL_INVENTORY_MOVEMENTS = "/v1/inventory_movements/";

// URLS CUSTOMERS
export const URL_CUSTOMERS = "/v1/customers/";
export const URL_ACTIVE_CUSTOMERS = `${URL_CUSTOMERS}active/`;
export const URL_INACTIVE_CUSTOMERS = `${URL_CUSTOMERS}inactive/`;

// URLS PROMOTIONS
export const URL_PROMOTIONS = "/v1/promotions/";
export const URL_ACTIVE_PROMOTIONS = `${URL_PROMOTIONS}active/`;
export const URL_INACTIVE_PROMOTIONS = `${URL_PROMOTIONS}inactive/`;

// URLS SALES
export const URL_SALES = "/v1/sales/";
export const URL_COMPLETED_SALES = `${URL_SALES}completed/`;
export const URL_CANCELED_SALES = `${URL_SALES}canceled/`;

// URLS INVOICES
export const URL_INVOICES = "/v1/invoices/";
export const URL_INVOICE_SALE = `${URL_INVOICES}sale/`;
export const URL_INVOICE_PURCHASE = `${URL_SALES}purchase/`;

// URLS SUPPLIERS
export const URL_SUPPLIERS = "/v1/suppliers/";
export const URL_ACTIVE_SUPPLIERS = `${URL_SUPPLIERS}active/`;
export const URL_INACTIVE_SUPPLIERS = `${URL_SUPPLIERS}inactive/`;

// URLS PURCHASES
export const URL_PURCHASES = "/v1/purchases/";
export const URL_COMPLETED_PURCHASES = `${URL_PURCHASES}completed/`;
export const URL_CANCELED_PURCHASES = `${URL_PURCHASES}canceled/`;

// URL CUSTOMER PROMOTIONS
export const URL_CUSTOMER_PROMOTIONS = "/v1/customer_promotions/";

// URLS SALE RETURNS
export const URL_SALE_RETURNS = "/v1/sale-returns/";
export const URL_COMPLETED_SALE_RETURNS = `${URL_SALE_RETURNS}completed/`;
export const URL_CANCELED_SALE_RETURNS = `${URL_SALE_RETURNS}canceled/`;

// URLS PURCHASE RETURNS
export const URL_PURCHASE_RETURNS = "/v1/purchase-returns/";
export const URL_COMPLETED_PURCHASE_RETURNS = `${URL_PURCHASE_RETURNS}completed/`;
export const URL_CANCELED_PURCHASE_RETURNS = `${URL_PURCHASE_RETURNS}canceled/`;

// URLS SALES REPORTS
export const URL_REPORTS_SALES = "/v1/reports/sales/";
export const URL_REPORTS_SALES_BY_CUSTOMER = `${URL_REPORTS_SALES}by-customer/`;
export const URL_REPORTS_SALES_BY_PAYMENT_METHOD = `${URL_REPORTS_SALES}by-payment-method/`;
export const URL_REPORTS_SALES_BY_PERIOD = `${URL_REPORTS_SALES}by-period/`;

// URLS PURCHASES REPORTS
export const URL_REPORTS_PURCHASES = "/v1/reports/purchases/";
export const URL_REPORTS_PURCHASES_BY_SUPPLIER = `${URL_REPORTS_PURCHASES}by-supplier/`;
export const URL_REPORTS_PURCHASES_BY_PERIOD = `${URL_REPORTS_PURCHASES}by-period/`;

// URLS CUSTOMERS REPORTS
export const URL_REPORTS_CUSTOMERS_PROMOTIONS = "/v1/reports/customers/promotions/";
export const URL_REPORTS_CUSTOMERS_TOP = "/v1/reports/customers/top/";

// URLS PRODUCTS REPORTS
export const URL_REPORTS_PRODUCTS_BY_CATEGORY = "/v1/reports/products/by-category/";
export const URL_REPORTS_PRODUCTS_LOW_SELLING = "/v1/reports/products/low-selling/";
export const URL_REPORTS_PRODUCTS_MOST_PURCHASED = "/v1/reports/products/most-purchased/";
export const URL_REPORTS_PRODUCTS_TOP_SELLING = "/v1/reports/products/top-selling/";

// URLS INVOICES REPORTS
export const URL_REPORTS_INVOICES = "/v1/reports/invoices/";
export const URL_REPORTS_INVOICES_SALES = "/v1/reports/invoices/sales/";
export const URL_REPORTS_INVOICES_PURCHASES = "/v1/reports/invoices/purchases/";

// URLS INVENTORIES REPORTS
export const URL_REPORTS_INVENTORIES = "/v1/reports/inventory/";
export const URL_REPORTS_INVENTORIES_LOW_STOCK = "/v1/reports/inventory/low-stock/";
export const URL_REPORTS_INVENTORIES_MOVEMENTS = "/v1/reports/inventory/movements/";

// KEYS
export const TOKEN_KEY = 'auth_token';
export const REFRESH_KEY = 'refresh_token';
export const USER_KEY = 'auth_user';
export const CSRFTOKEN_KEY = 'csrftoken';
