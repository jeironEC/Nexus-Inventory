import { parseHTML } from '../utils/dom.js';

// Gestiona notificaciones toast con iconos, tipos y auto-ocultado

class Toast {
    constructor() {
        this.container = document.getElementById('toast-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'toast-container';
            this.container.style.cssText = `
                position: fixed;
                top: 24px;
                right: 24px;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                gap: 12px;
                pointer-events: none;
            `;
            document.body.appendChild(this.container);
        }
    }

    // Muestra una notificación toast con mensaje y tipo
    show(message, type = 'success', duration = 4000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.style.pointerEvents = 'auto';

        const icon = this.getIcon(type);

        toast.appendChild(parseHTML(`
            <span class="material-symbols-outlined">${icon}</span>
            <div class="toast-content">${message}</div>
            <button class="toast-close">&times;</button>
        `));

        this.container.appendChild(toast);

        // Auto-ocultar después del tiempo especificado
        const timeout = setTimeout(() => {
            this.hide(toast);
        }, duration);

        // Botón de cierre manual
        toast.querySelector('.toast-close').addEventListener('click', () => {
            clearTimeout(timeout);
            this.hide(toast);
        });
    }

    // Oculta un toast con animación de desvanecimiento
    hide(toast) {
        toast.classList.add('toast-hiding');
        // Usar setTimeout si no hay animación CSS definida aún
        setTimeout(() => {
            if (toast.parentNode) toast.remove();
        }, 300);
    }

    // Obtiene el icono correspondiente según el tipo de notificación
    getIcon(type) {
        switch(type) {
            case 'success': return 'check_circle';
            case 'error': return 'error';
            case 'warning': return 'warning';
            case 'info': return 'info';
            default: return 'notifications';
        }
    }
}

export const toast = new Toast();
