export const DEFAULT_TIMEOUT = 3000;

// URLS ENDPOINTS
export const URL_BASE = "http://127.0.0.1:8000"
export const URL_AUTH_TOKEN = "/v1/auth/token/";
export const URL_AUTH_REFRESH = "/v1/auth/token/refresh/";
export const URL_USER = "/v1/users/";
export const URL_ACTIVE_USERS = "/v1/users/active/";
export const URL_INACTIVE_USERS = "/v1/users/inactive/";
export const URL_USER_PROFILE = "/v1/users/me/";
export const URL_ROLE = "/v1/roles/";
export const URL_ACTIVE_ROLES = "/v1/roles/active/";
export const URL_INACTIVE_ROLES = "/v1/roles/inactive/";

// KEYS
export const TOKEN_KEY = 'auth_token';
export const REFRESH_KEY = 'refresh_token';
export const USER_KEY = 'auth_user';
export const CSRFTOKEN_KEY = 'csrftoken';
