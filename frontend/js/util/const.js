export const DEFAULT_TIMEOUT = 3000;

// =========================================================================
// URLS ENDPOINTS
// =========================================================================

// URL BASE
export const URL_BASE = "http://127.0.0.1:8000";

// URLS TOKEN
export const URL_AUTH_TOKEN = "/v1/auth/token/";
export const URL_AUTH_REFRESH = "/v1/auth/token/refresh/";

// URLS USERS
export const URL_USERS = "/v1/users/";
export const URL_ACTIVE_USERS = "/v1/users/active/";
export const URL_INACTIVE_USERS = "/v1/users/inactive/";
export const URL_USERS_PROFILE = "/v1/users/me/";

// URLS ROLES
export const URL_ROLES = "/v1/roles/";
export const URL_ACTIVE_ROLES = "/v1/roles/active/";
export const URL_INACTIVE_ROLES = "/v1/roles/inactive/";

// URLS CATEGORIES
export const URL_CATEGORIES = "/v1/categories/";
export const URL_ACTIVE_CATEGORIES = "/v1/categories/active/";
export const URL_INACTIVE_CATEGORIES = "/v1/categories/inactive/";

// URLS PRODUCTS
export const URL_PRODUCTS = "/v1/products/";
export const URL_ACTIVE_PRODUCTS = "/v1/products/active/";
export const URL_INACTIVE_PRODUCTS = "/v1/products/inactive/";

// URLS INVENTORIES
export const URL_INVENTORIES = "/v1/inventories/";
export const URL_LOW_INVENTORIES = "/v1/inventories/low-stock/";
export const URL_PRODUCT_INVENTORIES = "/v1/inventories/product/";

// KEYS
export const TOKEN_KEY = 'auth_token';
export const REFRESH_KEY = 'refresh_token';
export const USER_KEY = 'auth_user';
export const CSRFTOKEN_KEY = 'csrftoken';
