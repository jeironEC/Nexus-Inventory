/**
 * PAGE_HEADER.JS
 * Componente del encabezado superior de todas las páginas.
 * Muestra: botón menú (móvil) + título + boton opcional + avatar + botón logout.
 *
 */

class PageHeader {
    constructor() {
        this.basePath = this.getBasePath();
    }

    getBasePath() {
        const path = window.location.pathname;
        if (path.endsWith('index.html') || path === '/' || path.endsWith('/')) return '';
        if (path.includes('/html/')) return '../';
        return '';
    }

    getUserInitials() {
        try {
            const user = JSON.parse(localStorage.getItem('auth_user') || '{}');
            let initials = '';
            if (user.first_name) initials += user.first_name[0];
            if (user.last_name)  initials += user.last_name[0];
            if (initials) return initials.toUpperCase();
            if (user.email) return user.email.substring(0, 2).toUpperCase();
        } catch (_) {}
        return 'NX';
    }

    createHeader(title, action) {
        const header = document.createElement('header');
        header.className = 'page-header';

        // Botón hamburguesa
        const menuToggle = document.createElement('button');
        menuToggle.className = 'btn-menu-toggle';
        menuToggle.setAttribute('aria-label', 'Abrir menú');

        const menuIcon = document.createElement('span');
        menuIcon.className = 'material-symbols-outlined';
        menuIcon.textContent = 'menu';
        menuToggle.appendChild(menuIcon);

        menuToggle.addEventListener('click', function () {
            if (window.sidebar && typeof window.sidebar.toggle === 'function') {
                window.sidebar.toggle();
            }
        });
        header.appendChild(menuToggle);

        // Título
        const titleEl = document.createElement('h1');
        titleEl.className = 'page-header-title';
        titleEl.textContent = title;
        header.appendChild(titleEl);

        // Acciones (lado derecho)
        const actions = document.createElement('div');
        actions.className = 'page-header-actions';

        // Botón de acción opcional
        if (action && action.text) {
            const actionBtn = document.createElement('button');
            actionBtn.className = 'btn btn-primary header-action-btn';
            actionBtn.id = 'header-action-btn';

            if (action.icon) {
                const icon = document.createElement('span');
                icon.className = 'material-symbols-outlined';
                icon.textContent = action.icon;
                actionBtn.appendChild(icon);
            }

            const text = document.createElement('span');
            text.textContent = action.text;
            actionBtn.appendChild(text);

            if (typeof action.onClick === 'function') {
                actionBtn.addEventListener('click', action.onClick);
            }

            actions.appendChild(actionBtn);
        }

        // Avatar
        const userBtn = document.createElement('button');
        userBtn.className = 'header-btn';
        userBtn.title = 'Ver perfil';

        const avatar = document.createElement('div');
        avatar.className = 'header-user-avatar';
        avatar.textContent = this.getUserInitials();
        userBtn.appendChild(avatar);

        userBtn.addEventListener('click', () => {
            window.location.href = this.basePath + 'html/profile.html';
        });

        // Logout
        const logoutBtn = document.createElement('button');
        logoutBtn.className = 'header-btn btn-logout';
        logoutBtn.setAttribute('aria-label', 'Cerrar sesión');
        logoutBtn.title = 'Cerrar sesión';

        const logoutIcon = document.createElement('span');
        logoutIcon.className = 'material-symbols-outlined';
        logoutIcon.textContent = 'logout';
        logoutBtn.appendChild(logoutIcon);

        logoutBtn.addEventListener('click', () => {
            if (window.modal && typeof window.modal.showConfirm === 'function') {
                window.modal.showConfirm(
                    'Cerrar Sesión',
                    '¿Deseas cerrar la sesión activa?',
                    () => {
                        window.location.href = this.basePath + 'html/login.html';
                    }
                );
            } else {
                window.location.href = this.basePath + 'html/login.html';
            }
        });

        actions.appendChild(userBtn);
        actions.appendChild(logoutBtn);
        header.appendChild(actions);

        return header;
    }

    init(title, action) {
        const container = document.getElementById('page-header-container');
        if (!container) return;

        while (container.firstChild) {
            container.removeChild(container.firstChild);
        }
        container.appendChild(this.createHeader(title, action));
    }
}

window.pageHeader = new PageHeader();
