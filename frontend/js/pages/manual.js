// Lógica de la página Manual de Uso

import { authService } from '../services/AuthService.js';

// Inicializa la página del manual
async function initManualPage() {
    if (!authService.isAuthenticated()) {
        window.location.href = '/index.html';
        return;
    }

    if (window.sidebar) {
        window.sidebar.init('manual.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Manual de Uso');
    }
}

document.addEventListener('DOMContentLoaded', initManualPage);
