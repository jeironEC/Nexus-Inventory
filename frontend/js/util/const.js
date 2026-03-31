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

// KEYS
export const TOKEN_KEY = 'auth_token';
export const REFRESH_KEY = 'refresh_token';
export const USER_KEY = 'auth_user';
export const CSRFTOKEN_KEY = 'csrftoken';
