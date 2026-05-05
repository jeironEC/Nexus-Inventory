// Motor RBAC para gestionar permisos por rol

export const ROLES = {
    ADMIN: 'admin',
    CASHIER: 'cajero',
    SALES: 'encargado de ventas',
    PURCHASES: 'encargado de compras'
};

// Rutas que todos los roles pueden ver
const COMMON_PAGES = ['dashboard.html', 'profile.html', 'index.html', 'terms.html', 'manual.html'];

export const ROLE_PERMISSIONS = {
    // Acceso total para admin
    [ROLES.ADMIN]: ['*'],

    [ROLES.CASHIER]: [
        ...COMMON_PAGES,
        'sales.html',
        'customers.html',
        'invoices.html',
        'sale_returns.html'
    ],

    [ROLES.SALES]: [
        ...COMMON_PAGES,
        'categories.html',
        'products.html',
        'customers.html',
        'sales.html',
        'sale_returns.html',
        'invoices.html',
        'reports/sales.html',
        'reports/customers.html',
        'reports/invoices.html'
    ],

    [ROLES.PURCHASES]: [
        ...COMMON_PAGES,
        'inventory.html',
        'categories.html',
        'products.html',
        'suppliers.html',
        'purchases.html',
        'purchase_returns.html',
        'invoices.html',
        'reports/purchases.html',
        'reports/inventory.html',
        'reports/products.html',
        'reports/invoices.html'
    ]
};

// Verifica si un rol tiene permiso para acceder a una página
export function hasPermission(roleName, pageId) {
    // Permitir acceso por defecto si el rol no está cargado
    if (!roleName) {
        return true;
    }

    const normalizedRole = roleName.trim().toLowerCase();
    const allowedPages = ROLE_PERMISSIONS[normalizedRole];
    if (!allowedPages) return false;

    // Admin tiene acceso total
    if (allowedPages.includes('*')) return true;

    const normalizedPageId = pageId.replace('html/', '').trim();
    return allowedPages.includes(normalizedPageId);
}

// Bloquea el acceso si el usuario no tiene permiso
export function enforcePermission(pageId) {
    if (!pageId || pageId === 'dashboard.html' || pageId === '') return;

    const alwaysAllowed = ['index.html', 'profile.html'];
    if (alwaysAllowed.includes(pageId)) return;

    const user = JSON.parse(localStorage.getItem('auth_user') || '{}');
    let role = user.role;

    if (typeof role === 'object' && role !== null) {
        role = role.name;
    }

    if (!role) return;

    if (!hasPermission(role, pageId)) {
        const isReport = window.location.pathname.includes('/html/reports/');
        const isHtml = window.location.pathname.includes('/html/');
        let indexPath = 'dashboard.html';
        if (isReport) indexPath = '../dashboard.html';
        else if (!isHtml) indexPath = 'html/dashboard.html';
        window.location.replace(indexPath);
    }
}

// Verifica si el usuario actual es administrador
export function isAdmin() {
    const user = JSON.parse(localStorage.getItem('auth_user') || '{}');
    let role = user.role;

    if (typeof role === 'object' && role !== null) {
        role = role.name;
    }

    if (!role) return false;
    return role.trim().toLowerCase() === ROLES.ADMIN;
}

// Oculta elementos según el rol usando atributos data-role
export function applyDeclarativeRBAC() {
    const user = JSON.parse(localStorage.getItem('auth_user') || '{}');
    let userRole = user.role;

    if (typeof userRole === 'object' && userRole !== null) {
        userRole = userRole.name;
    }

    if (!userRole) return;

    const normalizedRole = userRole.trim().toLowerCase();

    const elements = document.querySelectorAll('[data-role]');

    elements.forEach(el => {
        const requiredRoles = el.dataset.role.split(',').map(r => r.trim().toLowerCase());

        if (normalizedRole === ROLES.ADMIN) return;

        if (!requiredRoles.includes(normalizedRole)) {
            el.remove();
        }
    });
}
