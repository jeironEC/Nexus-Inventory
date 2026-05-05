// Constantes globales para URLs de API, configuraciones y almacenamiento
export const DEFAULT_TIMEOUT = 30000;


// URL base
export const URL_BASE = 'http://localhost:8000';

// URLs de endpoints de la API
// Auth
export const URL_AUTH_TOKEN = '/v1/auth/token/';
export const URL_AUTH_REFRESH = `${URL_AUTH_TOKEN}refresh/`;

// Password reset
export const URL_PASSWORD_RESET_REQUEST = '/v1/password-reset/request/';
export const URL_PASSWORD_RESET_VERIFY = '/v1/password-reset/verify/';
export const URL_PASSWORD_RESET_CONFIRM = '/v1/password-reset/confirm/';

// Users
export const URL_USERS = '/v1/users/';
export const URL_USERS_PROFILE = `${URL_USERS}me/`;

// Roles
export const URL_ROLES = '/v1/roles/';

// Categories
export const URL_CATEGORIES = '/v1/categories/';

// Companies
export const URL_COMPANIES = '/v1/companies/';

// Products
export const URL_PRODUCTS = '/v1/products/';

// Inventories
export const URL_INVENTORIES = '/v1/inventories/';
export const URL_LOW_INVENTORIES = `${URL_INVENTORIES}low-stock/`;
export const URL_PRODUCT_INVENTORIES = `${URL_INVENTORIES}product/`;

// Customers
export const URL_CUSTOMERS = '/v1/customers/';

// Sales
export const URL_SALES = '/v1/sales/';

// Invoices
export const URL_INVOICES = '/v1/invoices/';

// Suppliers
export const URL_SUPPLIERS = '/v1/suppliers/';

// Purchases
export const URL_PURCHASES = '/v1/purchases/';

// Sale returns
export const URL_SALE_RETURNS = '/v1/sale-returns/';

// Purchase returns
export const URL_PURCHASE_RETURNS = '/v1/purchase-returns/';

// Reports
export const URL_REPORTS_SALES = '/v1/reports/sales/';
export const URL_REPORTS_PURCHASES = '/v1/reports/purchases/';
export const URL_REPORTS_CUSTOMERS = '/v1/reports/customers/';
export const URL_REPORTS_PRODUCTS = '/v1/reports/products/';
export const URL_REPORTS_INVOICES = '/v1/reports/invoices/';
export const URL_REPORTS_INVENTORIES = '/v1/reports/inventory/';
export const URL_REPORTS_RETURNS = '/v1/reports/returns/';

// Configuraciones globales
export const DEFAULT_PAGINATION_LIMIT = 25;

// Keys de almacenamiento
export const TOKEN_KEY = 'auth_token';
export const REFRESH_KEY = 'refresh_token';
export const USER_KEY = 'auth_user';
export const CSRFTOKEN_KEY = 'csrftoken';
