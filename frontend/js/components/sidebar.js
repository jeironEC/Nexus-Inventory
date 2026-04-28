/**
 * SIDEBAR.JS
 * Componente de barra lateral.
 * Construye el sidebar dinámicamente y gestiona toggle en móvil.
 */

class Sidebar {
    constructor() {
        this.basePath = this.getBasePath();
    }

    getBasePath() {
        const path = window.location.pathname;
        if (path.endsWith('index.html') || path === '/' || path.endsWith('/')) return '';
        if (path.includes('/html/')) return '../';
        return '';
    }

    createSidebarItem(href, iconName, text, isActive) {
        const link = document.createElement('a');
        link.className = `sidebar-item${isActive ? ' active' : ''}`;
        link.href = href;

        const icon = document.createElement('span');
        icon.className = 'sidebar-icon material-symbols-outlined';
        icon.textContent = iconName;

        const textSpan = document.createElement('span');
        textSpan.className = 'sidebar-text';
        textSpan.textContent = text;

        link.appendChild(icon);
        link.appendChild(textSpan);
        return link;
    }

    createSidebarSection(label, items, activePage, base) {
        const section = document.createElement('div');
        section.className = 'sidebar-section';

        // Label de la sección
        const labelDiv = document.createElement('div');
        labelDiv.className = 'sidebar-section-label';

        const labelText = document.createElement('span');
        labelText.textContent = label;

        const arrowIcon = document.createElement('span');
        arrowIcon.className = 'material-symbols-outlined';
        arrowIcon.textContent = 'keyboard_arrow_down';

        labelDiv.appendChild(labelText);
        labelDiv.appendChild(arrowIcon);

        // Contenedor de items
        const itemsContainer = document.createElement('div');
        itemsContainer.className = 'sidebar-section-items';

        items.forEach(item => {
            const isActive = activePage === item.page;
            const link = this.createSidebarItem(`${base}${item.path}`, item.icon, item.text, isActive);
            itemsContainer.appendChild(link);
        });

        section.appendChild(labelDiv);
        section.appendChild(itemsContainer);

        // Toggle colapsar/expandir
        labelDiv.addEventListener('click', function () {
            section.classList.toggle('collapsed');
            arrowIcon.textContent = section.classList.contains('collapsed')
                ? 'keyboard_arrow_right'
                : 'keyboard_arrow_down';
        });

        return section;
    }

    build(activePage) {
        const base = this.basePath;

        const aside = document.createElement('aside');
        aside.className = 'sidebar';
        aside.id = 'sidebar';

        // Header con logo
        const header = document.createElement('div');
        header.className = 'sidebar-header';

        const logoText = document.createElement('span');
        logoText.className = 'sidebar-logo-text';
        logoText.appendChild(document.createTextNode('Nexus'));

        const logoEm = document.createElement('em');
        logoEm.textContent = 'Inventory';
        logoText.appendChild(logoEm);

        header.appendChild(logoText);
        aside.appendChild(header);

        // Navegación
        const nav = document.createElement('nav');
        nav.className = 'sidebar-nav';

        // ── Estructura del sidebar ──
        // Los items de cada sección se irán añadiendo página a página.
        const structure = [
            {
                label: 'Principal',
                items: [
                    { path: 'index.html',          page: 'index.html',     icon: 'dashboard',   text: 'Dashboard' },
                    { path: 'html/inventory.html', page: 'inventory.html', icon: 'inventory_2', text: 'Inventario' }
                ]
            },
            {
                label: 'Gestión',
                items: [
                    { path: 'html/users.html', page: 'users.html', icon: 'group', text: 'Usuarios' },
                    { path: 'html/roles.html', page: 'roles.html', icon: 'admin_panel_settings', text: 'Roles' },
                    { path: 'html/categories.html', page: 'categories.html', icon: 'category',  text: 'Categorías' },
                    { path: 'html/products.html', page: 'products.html', icon: 'inventory', text: 'Productos' }
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
                    { path: 'html/sale_returns.html', page: 'sale_returns.html', icon: 'assignment_return', text: 'Devoluciones Ventas' },
                    { path: 'html/purchase_returns.html', page: 'purchase_returns.html', icon: 'keyboard_return', text: 'Devoluciones Compras' }
                ]
            },
            {
                label: 'Reportes',
                items: [
                    { path: 'html/sales-report.html', page: 'reports/sales.html', icon: 'receipt_long', text: 'Reporte de Ventas' },
                    { path: 'html/purchases-report.html', page: 'reports/purchases.html', icon: 'shopping_bag', text: 'Reporte de Compras' },
                    { path: 'html/inventory-report.html', page: 'reports/inventory.html', icon: 'inventory_2', text: 'Reporte de Inventario' },
                    { path: 'html/products-report.html', page: 'reports/products.html', icon: 'list_alt', text: 'Reporte de Productos' },
                    { path: 'html/customers-report.html', page: 'reports/customers.html', icon: 'group', text: 'Reporte de Clientes' },
                    { path: 'html/returns-report.html', page: 'reports/returns.html', icon: 'assignment_return', text: 'Reporte de Devoluciones' }
                ]
            },
            {
                label: 'Sistema',
                items: [
                    { path: 'html/profile.html', page: 'profile.html', icon: 'person',    text: 'Perfil' },
                    { path: 'html/company.html', page: 'company.html', icon: 'business',    text: 'Perfil Empresa' },
                    { path: 'html/terms.html',   page: 'terms.html',   icon: 'description', text: 'Términos y Condiciones' },
                    { path: 'html/manual.html',  page: 'manual.html',  icon: 'menu_book',   text: 'Manual de Uso' }
                ]
            }
        ];

        structure.forEach(sectionData => {
            const sectionEl = this.createSidebarSection(sectionData.label, sectionData.items, activePage, base);
            nav.appendChild(sectionEl);
        });

        aside.appendChild(nav);
        return aside;
    }

    init(activePage) {
        const container = document.getElementById('sidebar-container');
        if (!container) return;

        // Vaciar contenedor sin innerHTML
        while (container.firstChild) {
            container.removeChild(container.firstChild);
        }

        container.appendChild(this.build(activePage));

        if (!document.querySelector('.sidebar-overlay')) {
            const overlay = document.createElement('div');
            overlay.className = 'sidebar-overlay';
            overlay.addEventListener('click', () => this.hide());
            document.body.appendChild(overlay);
        }
    }

    toggle() {
        const container = document.getElementById('sidebar-container');
        const overlay   = document.querySelector('.sidebar-overlay');
        if (container && overlay) {
            container.classList.toggle('active');
            overlay.classList.toggle('active');
        }
    }

    hide() {
        const container = document.getElementById('sidebar-container');
        const overlay   = document.querySelector('.sidebar-overlay');
        if (container && overlay) {
            container.classList.remove('active');
            overlay.classList.remove('active');
        }
    }
}

window.sidebar = new Sidebar();
