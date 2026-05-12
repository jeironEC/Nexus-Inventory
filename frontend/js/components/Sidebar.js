import { create, clearChildren } from '../utils/dom.js';
import { hasPermission } from '../utils/rbac.js';

// Gestiona la barra lateral de navegación con secciones colapsables y control de permisos

// Obtiene el rol del usuario desde el servicio
async function fetchUserRole() {
    try {
        const { userService } = await import('../services/UserService.js');
        const profileRes = await userService.getUserProfile();
        if (profileRes?.success && profileRes.data) {
            return typeof profileRes.data.role === 'object'
                ? profileRes.data.role?.name
                : profileRes.data.role;
        }
    } catch (err) {
    }
    return null;
}

let cachedRole = null;

// Obtiene el rol del usuario desde localStorage o servicio
function getCurrentUserRole() {
    try {
        const rawUser = localStorage.getItem('auth_user');
        if (!rawUser) {
            return cachedRole;
        }
        const user = JSON.parse(rawUser);

        let role = user.role;
        if (role === undefined || role === null) {
            if (!cachedRole) {
                fetchUserRole().then(role => {
                    cachedRole = role;
                });
            }
            return null;
        }

        if (typeof role === 'object') {
            role = role.name;
        }
        cachedRole = role;

        return role;
    } catch (err) {
        return null;
    }
}

class Sidebar {
    constructor() {
        this.basePath = this.getBasePath();
    }

    // Determina la ruta base según la ubicación actual
    getBasePath() {
        const path = window.location.pathname;
        if (path === '/' || path.endsWith('/') || (path.endsWith('index.html') && !path.includes('/html/'))) {
            return '';
        }
        if (path.includes('/html/reports/')) {
            return '../../';
        }
        if (path.includes('/html/')) {
            return '../';
        }
        return '';
    }

    // Crea un elemento de enlace para el sidebar
    createSidebarItem(href, iconName, text, isActive) {
        const link = create('a', `sidebar-item ${isActive ? 'active' : ''}`, { href });
        const icon = create('span', 'sidebar-icon material-symbols-outlined', {}, iconName);
        const textSpan = create('span', 'sidebar-text', {}, text);

        link.appendChild(icon);
        link.appendChild(textSpan);
        return link;
    }

    // Crea una sección del sidebar con sus elementos filtrados por permisos
    createSidebarSection(label, items, activePage, base) {
        const section = create('div', 'sidebar-section');

        const labelDiv = create('div', 'sidebar-section-label');
        const labelSpan = create('span', '', {}, label);
        const arrowIcon = create('span', 'material-symbols-outlined', {}, 'keyboard_arrow_down');

        labelDiv.appendChild(labelSpan);
        labelDiv.appendChild(arrowIcon);

        const itemsContainer = create('div', 'sidebar-section-items');

        const userRole = getCurrentUserRole();

        items.forEach(item => {
            if (!hasPermission(userRole, item.page)) return;

            const isActive = activePage === item.page;
            const link = this.createSidebarItem(`${base}${item.path}`, item.icon, item.text, isActive);
            itemsContainer.appendChild(link);
        });

        section.appendChild(labelDiv);
        section.appendChild(itemsContainer);

        // Si no quedaron items visibles, no renderizar la sección
        if (itemsContainer.children.length === 0) return null;

        labelDiv.addEventListener('click', function handleSectionToggle() {
            section.classList.toggle('collapsed');
            arrowIcon.textContent = section.classList.contains('collapsed')
                ? 'keyboard_arrow_right'
                : 'keyboard_arrow_down';
        });

        return section;
    }

    // Construye el sidebar completo como un nodo HTMLElement
    build(activePage) {
        const base = this.basePath;
        const aside = create('aside', 'sidebar', { id: 'sidebar' });

        // Encabezado del logo con link al dashboard
        const header = create('div', 'sidebar-header');
        const logoLink = create('a', 'sidebar-logo-link', { href: `${base}html/dashboard.html`, style: 'text-decoration: none; display: flex; align-items: center;' });
        const logoText = create('span', 'sidebar-logo-text', {}, 'Nexus');
        const inventoryEm = create('em', '', {}, 'Inventory');

        logoText.appendChild(inventoryEm);
        logoLink.appendChild(logoText);
        header.appendChild(logoLink);
        aside.appendChild(header);

        // Contenedor de navegación
        const nav = create('nav', 'sidebar-nav');

        // Estructura de secciones y enlaces
        const structure = [
            {
                label: 'Principal',
                items: [
                    { path: 'html/dashboard.html', page: 'dashboard.html', icon: 'dashboard', text: 'Dashboard' },
                    { path: 'html/inventory.html', page: 'inventory.html', icon: 'inventory_2', text: 'Inventario' },
                    { path: 'html/inventory_movements.html', page: 'inventory_movements.html', icon: 'swap_horiz', text: 'Movimientos' }
                ]
            },
            {
                label: 'Gestión',
                items: [
                    { path: 'html/users.html', page: 'users.html', icon: 'group', text: 'Usuarios' },
                    { path: 'html/roles.html', page: 'roles.html', icon: 'admin_panel_settings', text: 'Roles' },
                    { path: 'html/categories.html', page: 'categories.html', icon: 'category', text: 'Categorías' },
                    { path: 'html/products.html', page: 'products.html', icon: 'inventory', text: 'Productos' },
                ]
            },
            {
                label: 'Negocios',
                items: [
                    { path: 'html/customers.html', page: 'customers.html', icon: 'people', text: 'Clientes' },
                    { path: 'html/suppliers.html', page: 'suppliers.html', icon: 'local_shipping', text: 'Proveedores' },
                    { path: 'html/sales.html', page: 'sales.html', icon: 'point_of_sale', text: 'Ventas' },
                    { path: 'html/purchases.html', page: 'purchases.html', icon: 'shopping_cart', text: 'Compras' },
                    { path: 'html/invoices.html', page: 'invoices.html', icon: 'receipt_long', text: 'Facturas' },
                    { path: 'html/sale_returns.html', page: 'sale_returns.html', icon: 'assignment_return', text: 'Ventas: Devol.' },
                    { path: 'html/purchase_returns.html', page: 'purchase_returns.html', icon: 'keyboard_return', text: 'Compras: Devol.' },
                ]
            },
            {
                label: 'Reportes',
                items: [
                    { path: 'html/reports/sales.html', page: 'reports/sales.html', icon: 'receipt_long', text: 'Reporte de Ventas' },
                    { path: 'html/reports/purchases.html', page: 'reports/purchases.html', icon: 'shopping_bag', text: 'Reporte de Compras' },
                    { path: 'html/reports/inventory.html', page: 'reports/inventory.html', icon: 'inventory', text: 'Reporte de Inventario' },
                    { path: 'html/reports/products.html', page: 'reports/products.html', icon: 'list_alt', text: 'Reporte de Productos' },
                    { path: 'html/reports/customers.html', page: 'reports/customers.html', icon: 'group', text: 'Reporte de Clientes' },
                    { path: 'html/reports/returns.html', page: 'reports/returns.html', icon: 'assignment_return', text: 'Reporte de Devoluciones' },
                    { path: 'html/reports/invoices.html', page: 'reports/invoices.html', icon: 'article', text: 'Reporte de Facturas' }
                ]
            },
            {
                label: 'Sistema',
                items: [
                    { path: 'html/profile.html', page: 'profile.html', icon: 'person', text: 'Mi Perfil' },
                    { path: 'html/company.html', page: 'company.html', icon: 'business', text: 'Empresa' },
                    { path: 'html/terms.html', page: 'terms.html', icon: 'docs', text: 'Términos y condiciones' },
                    { path: 'html/manual.html', page: 'manual.html', icon: 'menu_book', text: 'Manual de Uso' }
                ]
            }
        ];

        structure.forEach(sectionData => {
            const sectionEl = this.createSidebarSection(sectionData.label, sectionData.items, activePage, base);
            if (sectionEl) nav.appendChild(sectionEl);
        });

        aside.appendChild(nav);
        return aside;
    }

    // Inicializa el sidebar inyectándolo en el DOM y crea el overlay
    init(activePage) {
        const sidebarContainer = document.getElementById('sidebar-container');
        if (!sidebarContainer) {
            return;
        }

        clearChildren(sidebarContainer);
        const sidebarNode = this.build(activePage);
        sidebarContainer.appendChild(sidebarNode);

        // Crear e inyectar el overlay si no existe
        if (!document.querySelector('.sidebar-overlay')) {
            const overlay = create('div', 'sidebar-overlay');
            overlay.addEventListener('click', () => this.hide());
            document.body.appendChild(overlay);
        }
    }

    // Alterna la visibilidad del sidebar en móviles
    toggle() {
        const sidebar = document.getElementById('sidebar-container');
        const overlay = document.querySelector('.sidebar-overlay');
        if (sidebar && overlay) {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        }
    }

    // Oculta el sidebar en móviles
    hide() {
        const sidebar = document.getElementById('sidebar-container');
        const overlay = document.querySelector('.sidebar-overlay');
        if (sidebar && overlay) {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        }
    }
}

// Exponer instancia global para uso en la aplicación
window.sidebar = new Sidebar();
