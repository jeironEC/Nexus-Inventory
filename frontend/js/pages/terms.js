// Lógica de la página Términos y Condiciones

import { authService } from '../services/AuthService.js';

// Inicializa la página de términos y condiciones
async function initTermsPage() {
    if (!authService.isAuthenticated()) {
        window.location.href = '/index.html';
        return;
    }

    if (window.sidebar) {
        window.sidebar.init('terms.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Términos y Condiciones');
    }
}

document.addEventListener('DOMContentLoaded', initTermsPage);
