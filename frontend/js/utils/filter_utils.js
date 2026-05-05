// Utilidades centralizadas para filtros de búsqueda

import { renderHTML } from './dom.js';

// Mapa de filtros: ID del select -> configuración
const FILTER_SELECT_MAP = {
    'inventory-filter-product-id': {
        serviceKey: 'products',
        label: (item) => item.name || `Producto #${item.id}`,
        value: (item) => item.id,
        placeholder: 'Todos los productos'
    },
    'sale-filter-customer-id': {
        serviceKey: 'customers',
        label: (item) => `${item.first_name || ''} ${item.last_name || ''}`.trim() || `Cliente #${item.id}`,
        value: (item) => item.id,
        placeholder: 'Todos los clientes',
        extraOption: { value: 'anonymous', label: 'Anónimo' }
    },
    'purchase-filter-supplier-id': {
        serviceKey: 'suppliers',
        label: (item) => item.name || `Proveedor #${item.id}`,
        value: (item) => item.id,
        placeholder: 'Todos los proveedores'
    },
    'sale-return-filter-sale-id': {
        serviceKey: 'sales',
        label: (item) => `Venta #${item.id}`,
        value: (item) => item.id,
        placeholder: 'Todas las ventas'
    },
    'purchase-return-filter-purchase-id': {
        serviceKey: 'purchases',
        label: (item) => `Compra #${item.id}`,
        value: (item) => item.id,
        placeholder: 'Todas las compras'
    },
    'invoice-filter-sale-id': {
        serviceKey: 'sales',
        label: (item) => `Venta #${item.id}`,
        value: (item) => item.id,
        placeholder: 'Todas las ventas'
    },
    'invoice-filter-purchase-id': {
        serviceKey: 'purchases',
        label: (item) => `Compra #${item.id}`,
        value: (item) => item.id,
        placeholder: 'Todas las compras'
    },
    'user-filter-role-id': {
        serviceKey: 'roles',
        label: (item) => item.name || `Rol #${item.id}`,
        value: (item) => item.id,
        placeholder: 'Todos los roles'
    },
    'product-filter-category-id': {
        serviceKey: 'categories',
        label: (item) => item.name || `Categoría #${item.id}`,
        value: (item) => item.id,
        placeholder: 'Todas las categorías'
    }
};

// Lee valores de inputs y selects en un contenedor
export function getFilterValues(containerSelector) {
    const container = typeof containerSelector === 'string'
        ? document.querySelector(containerSelector)
        : containerSelector;
    if (!container) return {};

    const values = {};
    container.querySelectorAll('input, select, textarea').forEach(el => {
        const rawKey = el.id || el.name;
        if (!rawKey || !el.value) return;

        let key = rawKey;
        if (rawKey.startsWith('report-filter-')) {
            key = rawKey.replace('report-filter-', '').replace(/-/g, '_');
        } else if (rawKey.includes('-filter-')) {
            key = rawKey.replace(/^.+-filter-/, '').replace(/-/g, '_');
        }

        if (el.type === 'date' || el.type === 'datetime-local') {
            values[key] = el.value;
        } else if (key === 'payment_method') {
            values[key] = el.value.toUpperCase();
        } else {
            const num = parseFloat(el.value);
            values[key] = isNaN(num) ? el.value : num;
        }
    });

    return values;
}

// Inicializa listeners para aplicar filtros
export function initFilterListeners(containerSelector, callback) {
    const btnApply = document.getElementById('btn-apply-filters');
    if (btnApply) {
        btnApply.addEventListener('click', () => {
            if (typeof callback === 'function') callback();
        });
    }

    const container = typeof containerSelector === 'string'
        ? document.querySelector(containerSelector)
        : document.body;

    if (container) {
        container.querySelectorAll('select.no-dynamic').forEach(select => {
            select.addEventListener('change', () => {
                if (typeof callback === 'function') callback();
            });
        });
    }

    _addResetButton(containerSelector, callback);
    _initChoicesAll(containerSelector);
}

// Limpia todos los filtros a su estado inicial
export function resetFilters(containerSelector, callback) {
    const container = typeof containerSelector === 'string'
        ? document.querySelector(containerSelector)
        : containerSelector;
    if (!container) return;

    container.querySelectorAll('input, select, textarea').forEach(el => {
        if (el.type === 'checkbox' || el.type === 'radio') {
            el.checked = false;
        } else if (el.tagName === 'SELECT') {
            if (el._choices && typeof el._choices.destroy === 'function') {
                el._choices.destroy();
                delete el._choices;
            }
            const firstOption = el.querySelector('option:first-of-type');
            if (firstOption) {
                el.value = firstOption.value || '';
            } else {
                el.value = '';
            }
        } else {
            el.value = '';
        }
    });

    if (typeof callback === 'function') callback();

    setTimeout(() => _initChoicesAll(containerSelector), 50);
}

// Agrega botón de restaurar filtros dinámicamente
function _addResetButton(containerSelector, callback) {
    const btnApply = document.getElementById('btn-apply-filters');
    if (!btnApply) return;

    const filterActions = btnApply.closest('.filter-actions');
    if (!filterActions || filterActions.querySelector('.btn-reset-filters')) return;

    filterActions.classList.add('has-reset');

    const btnReset = document.createElement('button');
    btnReset.type = 'button';
    btnReset.className = 'btn btn-secondary btn-reset-filters';
    btnReset.innerHTML = `
        <span class="material-symbols-outlined">restart_alt</span>
        Restaurar
    `;
    btnReset.addEventListener('click', () => {
        resetFilters(containerSelector, callback);
    });

    filterActions.appendChild(btnReset);
}

// Inicializa Choices.js en todos los selects de filtros
function _initChoicesAll(containerSelector) {
    const container = typeof containerSelector === 'string'
        ? document.querySelector(containerSelector)
        : document.body;

    if (!container) return;

    container.querySelectorAll('.form-select').forEach(select => {
        if (select.classList.contains('no-choices')) return;
        if (select.dataset.choicesInitialized) return;

        _initChoices(select);
    });
}

// Carga dinámicamente datos de selects de filtros
export async function loadFilterSelects(filterIds) {
    const { serviceProvider } = await import('../services/ServiceProvider.js');

    for (const filterId of filterIds) {
        const selectEl = document.getElementById(filterId);
        if (!selectEl) continue;

        const config = FILTER_SELECT_MAP[filterId];
        if (!config) {
            continue;
        }

        selectEl.disabled = true;
        renderHTML(selectEl, `<option value="">Cargando...</option>`);

        try {
            const service = serviceProvider[config.serviceKey];
            if (!service) {
                continue;
            }

            const response = await service.getAll({ limit: 500 });
            const items = response?.data?.results || (Array.isArray(response?.data) ? response.data : []);

            let optionsHTML = `<option value="">${config.placeholder || 'Todos'}</option>`;
            if (config.extraOption) {
                optionsHTML += `<option value="${config.extraOption.value}">${config.extraOption.label}</option>`;
            }
            items.forEach(item => {
                optionsHTML += `<option value="${config.value(item)}">${config.label(item)}</option>`;
            });

            renderHTML(selectEl, optionsHTML);
            selectEl.disabled = false;

            _initChoices(selectEl);

        } catch (err) {
            renderHTML(selectEl, `<option value="">Error al cargar</option>`);
            selectEl.disabled = false;
        }
    }
}

// Inicializa Choices.js en un select individual
function _initChoices(selectEl) {
    try {
        if (typeof Choices === 'undefined') return;

        if (selectEl._choices) {
            selectEl._choices.destroy();
            delete selectEl._choices;
            selectEl.removeAttribute('data-choices-initialized');
        }

        const choices = new Choices(selectEl, {
            searchEnabled: true,
            itemSelectText: '',
            noResultsText: 'Sin resultados',
            noChoicesText: 'Sin opciones',
            shouldSort: false,
            searchPlaceholderValue: 'Buscar...',
            placeholder: false
        });

        selectEl._choices = choices;
        selectEl.dataset.choicesInitialized = 'true';
    } catch (e) {
    }
}
