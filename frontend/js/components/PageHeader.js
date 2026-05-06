import { create, clearChildren, parseHTML } from '../utils/dom.js';
import { getInitials } from '../utils/helpers.js';
import { authService } from '../services/AuthService.js';
import { enforcePermission } from '../utils/rbac.js';

// Gestiona el encabezado superior de las páginas con navegación y controles de usuario

// Extrae el pageId relativo de la URL actual
function getCurrentPageId() {
    const pathname = window.location.pathname;

    // Caso: estamos en /html/reports/xxx.html
    const reportsMatch = pathname.match(/\/html\/reports\/([^/]+\.html)/);
    if (reportsMatch) return `reports/${reportsMatch[1]}`;

    // Caso: estamos en /html/xxx.html
    const htmlMatch = pathname.match(/\/html\/([^/]+\.html)/);
    if (htmlMatch) return htmlMatch[1];

    // Caso: index.html o raíz
    return 'index.html';
}

class PageHeader {
    constructor() {
        this.basePath = this.getBasePath();
    }

    // Determina la ruta base según la ubicación actual
    getBasePath() {
        const path = window.location.pathname;
        if (path.endsWith('index.html') || path === '/' || path.endsWith('/')) {
            return '';
        }
        if (path.includes('/reports/')) {
            return '../../';
        }
        if (path.includes('/')) {
            return '../';
        }
        return '';
    }

    // Obtiene las iniciales del usuario logueado
    getUserAvatarHTML() {
        try {
            const user = JSON.parse(localStorage.getItem('auth_user') || '{}');

            const initials = getInitials(user);

            if (initials) {
                return initials;
            }
        } catch (e) {
        }
        return `<span class="material-symbols-outlined" style="font-size: 18px;">person</span>`;
    }

    // Crea los elementos del encabezado
    createHeader(title, options = {}) {
        const { showActions = true, extraActions = null } = options;
        const header = create('header', 'page-header');

        const menuToggle = create('button', 'btn-menu-toggle', {
            'aria-label': 'Abrir menú',
            'type': 'button'
        });
        menuToggle.appendChild(parseHTML('<span class="material-symbols-outlined">menu</span>'));
        menuToggle.addEventListener('click', () => {
            if (window.sidebar && typeof window.sidebar.toggle === 'function') {
                window.sidebar.toggle();
            }
        });
        header.appendChild(menuToggle);

        const titleEl = create('h1', 'page-header-title', {}, title);
        header.appendChild(titleEl);

        const actionsContainer = create('div', 'page-header-actions');

        if (extraActions) {
            if (Array.isArray(extraActions)) {
                extraActions.forEach(action => actionsContainer.appendChild(action));
            } else {
                actionsContainer.appendChild(extraActions);
            }
        }

        if (showActions) {
            const userBtn = create('button', 'header-btn', { title: 'Ver Perfil' });
            const userAvatar = create('div', 'header-user-avatar');
            userAvatar.appendChild(parseHTML(this.getUserAvatarHTML()));
            userBtn.appendChild(userAvatar);

            userBtn.addEventListener('click', () => {
                window.location.href = '/html/profile.html';
            });

            const logoutBtn = create('button', 'header-btn btn-logout', {
                title: 'Cerrar sesión',
                'aria-label': 'Cerrar sesión'
            });
            const logoutIcon = create('span', 'material-symbols-outlined', {}, 'logout');
            logoutBtn.appendChild(logoutIcon);

            actionsContainer.appendChild(userBtn);
            actionsContainer.appendChild(logoutBtn);
        }

        actionsContainer.appendChild(parseHTML(''));
        header.appendChild(actionsContainer);
        return header;
    }

    // Renderiza el encabezado y ejecuta el guard RBAC
    init(title, options = {}) {
        // GUARD RBAC
        const pageId = getCurrentPageId();
        // Las páginas de login se excluyen del guard
        if (!pageId.includes('login')) {
            enforcePermission(pageId);
        }

        const headerContainer = document.getElementById('page-header-container');
        if (!headerContainer) {
            return;
        }

        clearChildren(headerContainer);
        const header = this.createHeader(title, options);
        headerContainer.appendChild(header);

        // Configurar listener de logout
        const logoutBtn = headerContainer.querySelector('.btn-logout');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                if (window.modal && typeof window.modal.showConfirm === 'function') {
                    window.modal.showConfirm(
                        'Cerrar Sesión',
                        '¿Deseas cerrar la sesión activa?',
                        () => {
                            authService.logout();
                            window.location.href = '/index.html';
                        }
                    );
                } else {
                    authService.logout();
                    window.location.href = '/index.html';
                }
            });
        }
    }
}

// Exportar instancia única para toda la aplicación
window.pageHeader = new PageHeader();
export const pageHeader = window.pageHeader;
