// Utilidades de formateo y validación de datos

// Formatea fecha según el formato indicado
export function formatDate(date, format = 'dd/mm/yyyy') {
    const d = new Date(date);

    if (isNaN(d.getTime())) {
        return '';
    }

    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');

    switch (format) {
        case 'yyyy-mm-dd':
            return `${year}-${month}-${day}`;
        case 'yyyy-mm-dd HH:mm':
            return `${year}-${month}-${day} ${hours}:${minutes}`;
        case 'dd/mm/yyyy':
            return `${day}/${month}/${year}`;
        case 'dd/mm/yyyy HH:mm':
            return `${day}/${month}/${year} ${hours}:${minutes}`;
        case 'HH:mm':
            return `${hours}:${minutes}`;
        case 'full':
            return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
        default:
            return `${day}/${month}/${year}`;
    }
}

// Formatea cantidad como moneda (€ por defecto)
export function formatCurrency(amount, currency = '€') {
    if (amount === null || amount === undefined || isNaN(amount)) {
        return `${currency} 0,00`;
    }

    const formatted = Number(amount).toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return `${currency} ${formatted}`;
}

// Formatea número con separador de miles
export function formatNumber(number) {
    if (number === null || number === undefined || isNaN(number)) {
        return '0';
    }

    return Number(number).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

// Obtiene las iniciales de un nombre u objeto usuario
export function getInitials(user) {
    if (!user) return '';

    let firstName = '';
    let lastName = '';

    if (typeof user === 'string') {
        const parts = user.trim().split(' ');
        if (parts.length >= 2) {
            return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
        }
        return parts[0].charAt(0).toUpperCase();
    } else {
        firstName = user.first_name || '';
        lastName = user.last_name || '';
    }

    let initials = '';
    if (firstName.trim()) initials += firstName.trim()[0];
    if (lastName.trim()) initials += lastName.trim()[0];

    return initials.toUpperCase();
}

// Configura el estado de carga de un botón (loading/normal)
export function setButtonLoading(button, isLoading, originalContent = null) {
    if (!button) return null;

    if (isLoading) {
        button.disabled = true;
        const spinnerIcon = document.createElement('span');
        spinnerIcon.className = 'material-symbols-outlined spinner';
        spinnerIcon.textContent = 'sync';

        const textNode = document.createTextNode(' Cargando...');

        // Guardar contenido original si no se proporcionó
        const original = originalContent || Array.from(button.childNodes);

        // Limpiar y mostrar spinner
        while (button.firstChild) {
            button.removeChild(button.firstChild);
        }
        button.appendChild(spinnerIcon);
        button.appendChild(textNode);

        return original;
    } else {
        button.disabled = false;
        // Si se pasó contenido original específico, usarlo
        if (originalContent && Array.isArray(originalContent)) {
            while (button.firstChild) {
                button.removeChild(button.firstChild);
            }
            originalContent.forEach(node => button.appendChild(node));
        }
        return null;
    }
}

// Devuelve el nombre completo formateado
export function formatFullName(user) {
    if (!user) return '';
    return `${user.first_name || ''} ${user.last_name || ''}`.trim();
}

// Valida formato de email
export function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Actualiza elementos KPI en un contenedor basándose en data-kpi
export function updateKPIs(container, data, formatters = {}) {
    const root = typeof container === 'string' ? document.querySelector(container) : container;
    if (!root || !data) return;

    const kpiElements = root.querySelectorAll('[data-kpi]');
    kpiElements.forEach(el => {
        const key = el.dataset.kpi;
        if (data[key] !== undefined) {
            const value = data[key];
            const formatter = formatters[key] || (val => val);
            el.textContent = formatter(value);
        }
    });
}
