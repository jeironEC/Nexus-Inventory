/**
 * PAGE_HEADER.JS
 * Componente del encabezado superior de todas las páginas.
 * Muestra: botón menú (móvil) + título + avatar + botón logout.
 * El logout por ahora redirige a login.html a través de un modal de confirmación.
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

    createHeader(title) {
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

        // Acciones
        const actions = document.createElement('div');
        actions.className = 'page-header-actions';

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

    init(title) {
        const container = document.getElementById('page-header-container');
        if (!container) return;

        while (container.firstChild) {
            container.removeChild(container.firstChild);
        }
        container.appendChild(this.createHeader(title));
    }
}

window.pageHeader = new PageHeader();
