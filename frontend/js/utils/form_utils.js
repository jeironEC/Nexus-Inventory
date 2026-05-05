// Utilidades para manejo de formularios

import { parseHTML, renderHTML, clearChildren } from './dom.js';

// Rellena un formulario con datos de un objeto
export function fillForm(form, data) {
    if (!form || !data) return;

    Object.keys(data).forEach(key => {
        const input = form.elements[key];
        if (!input) return;

        let value = data[key];

        // Manejar objetos anidados (ej. product.category.id)
        if (value && typeof value === 'object' && value.id !== undefined) {
            value = value.id;
        }

        if (input.type === 'checkbox') {
            input.checked = !!value;
        } else {
            input.value = value !== null ? value : '';
        }
    });
}

// Extrae datos de un formulario como objeto
export function getFormData(form) {
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    return data;
}

// Configura filas dinámicas para detalles de ventas/compras
export function setupDynamicDetails({
    containerId,
    btnAddId,
    template,
    products,
    onProductSelect = null,
    onRowAdded = null
}) {
    const container = document.getElementById(containerId);
    const btnAdd = document.getElementById(btnAddId);

    if (!container || !btnAdd) return;

    const isTable = container.tagName === 'TBODY';

    const getVal = (row, name) => {
        const el = row.querySelector(`[name="${name}"]`);
        return el ? parseFloat(el.value) || 0 : 0;
    };

    const recalcRow = (row) => {
        const quantity = getVal(row, 'quantity');
        const price = getVal(row, 'unit_price') || getVal(row, 'unit_cost');
        const discount = getVal(row, 'discount_percentage');

        const base = quantity * price;
        const subtotal = base - (base * discount / 100);

        const subtotalEl = row.querySelector('.sale-detail-subtotal, .purchase-detail-subtotal');
        if (subtotalEl) {
            subtotalEl.textContent = `€ ${subtotal.toFixed(2)}`;
            subtotalEl.dataset.value = subtotal;
        }

        return subtotal;
    };

    const recalcAll = () => {
        const rows = isTable ? container.querySelectorAll('tr') : container.querySelectorAll('.detail-row');
        let total = 0;
        rows.forEach(row => {
            total += recalcRow(row);
        });

        const saleSubtotal = document.getElementById('sale-subtotal');
        const saleTax = document.getElementById('sale-tax');
        const saleTotal = document.getElementById('sale-total');
        if (saleSubtotal) {
            saleSubtotal.textContent = `€ ${total.toFixed(2)}`;
            const iva = parseFloat(document.getElementById('new-sale-iva')?.value || 0);
            const taxAmount = total * iva / 100;
            if (saleTax) saleTax.textContent = `€ ${taxAmount.toFixed(2)}`;
            if (saleTotal) saleTotal.textContent = `€ ${(total + taxAmount).toFixed(2)}`;
        }

        const purchaseSubtotal = document.getElementById('purchase-subtotal');
        const purchaseTax = document.getElementById('purchase-tax');
        const purchaseTotal = document.getElementById('purchase-total');
        if (purchaseSubtotal) {
            purchaseSubtotal.textContent = `€ ${total.toFixed(2)}`;
            const iva = parseFloat(document.getElementById('new-purchase-iva')?.value || 0);
            const taxAmount = total * iva / 100;
            if (purchaseTax) purchaseTax.textContent = `€ ${taxAmount.toFixed(2)}`;
            if (purchaseTotal) purchaseTotal.textContent = `€ ${(total + taxAmount).toFixed(2)}`;
        }
    };

    const setupRow = (row) => {
        const select = row.querySelector('select[name="product"], select[name="product_id"]');
        if (select) {
            populateSelectSimple(select, products, 'name', 'id');
            select.addEventListener('change', () => {
                const product = products.find(p => p.id == select.value);
                if (product && onProductSelect) {
                    onProductSelect(product, row);
                }
                recalcAll();
            });
        }

        ['quantity', 'unit_price', 'unit_cost', 'discount_percentage'].forEach(name => {
            const input = row.querySelector(`input[name="${name}"]`);
            if (input) {
                input.addEventListener('input', recalcAll);
                input.addEventListener('change', recalcAll);
            }
        });

        row.querySelector('.btn-remove-detail')?.addEventListener('click', () => {
            const allRows = isTable ? container.querySelectorAll('tr') : container.querySelectorAll('.detail-row');
            if (allRows.length > 1) {
                row.remove();
                recalcAll();
            }
        });

        recalcRow(row);
    };

    // Poblar selects en filas ya existentes
    const existingRows = isTable ? container.querySelectorAll('tr') : container.querySelectorAll('.detail-row');
    existingRows.forEach(setupRow);

    const addRow = () => {
        let row;

        if (isTable) {
            // Parsear el template completo como <tr> usando un wrapper de tabla
            const wrapper = document.createElement('div');
            wrapper.innerHTML = `<table><tbody>${template}</tbody></table>`;
            row = wrapper.querySelector('tr');
        } else {
            row = document.createElement('div');
            row.className = 'detail-row';
            row.appendChild(parseHTML(template));
        }

        setupRow(row);

        container.appendChild(row);
        if (onRowAdded) onRowAdded(row);
        return row;
    };

    btnAdd.addEventListener('click', (e) => {
        e.preventDefault();
        addRow();
    });

    const ivaInput = document.getElementById('new-sale-iva') || document.getElementById('new-purchase-iva');
    if (ivaInput) {
        ivaInput.addEventListener('input', recalcAll);
        ivaInput.addEventListener('change', recalcAll);
    }

    recalcAll();

    return { addRow };
}

// Rellena un select sin Choices.js (para filas de tabla)
export function populateSelectSimple(select, items, textKey = 'name', valueKey = 'id', selectedValue = null) {
    if (!select) return;
    clearChildren(select);

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Seleccionar...';
    defaultOption.selected = true;
    defaultOption.disabled = true;
    select.appendChild(defaultOption);

    items.forEach(item => {
        const opt = document.createElement('option');
        opt.value = item[valueKey];
        if (textKey === 'full_name' && item.first_name) {
            opt.textContent = `${item.first_name} ${item.last_name || ''}`.trim();
        } else if (typeof textKey === 'function') {
            opt.textContent = textKey(item);
        } else {
            opt.textContent = item[textKey] || `#${item[valueKey]}`;
        }
        select.appendChild(opt);
    });

    if (selectedValue !== null && selectedValue !== undefined) {
        select.value = selectedValue;
    }
}

// Extrae datos de filas dinámicas
export function getRowsData(containerId, fieldNames) {
    const container = document.getElementById(containerId);
    if (!container) return [];

    const isTable = container.tagName === 'TBODY';
    const rows = isTable ? container.querySelectorAll('tr') : container.querySelectorAll('.detail-row');
    const data = [];

    rows.forEach(row => {
        const rowData = {};
        let hasValue = false;

        fieldNames.forEach(field => {
            const el = row.querySelector(`[name="${field}"]`);
            if (el) {
                const val = el.value;
                // Intentar convertir a número si es tipo number
                if (el.type === 'number') {
                    rowData[field] = val.includes('.') ? parseFloat(val) : parseInt(val);
                } else {
                    rowData[field] = val;
                }
                if (val) hasValue = true;
            }
        });

        if (hasValue) data.push(rowData);
    });

    return data;
}

// Puebla un select con opciones genéricas
export function populateSelect(select, items, textKey = 'name', valueKey = 'id', selectedValue = null) {
    if (!select) return;

    // Si selectedValue está definido y es válido, usarlo
    const targetVal = (selectedValue !== null && selectedValue !== undefined && selectedValue !== '') ? String(selectedValue) : null;

    // Destruir instancia de Choices antes de modificar el DOM
    if (select._choices) {
        try { select._choices.destroy(); } catch(e) {}
        select._choices = null;
        delete select.dataset.choicesInitialized;
    }

    clearChildren(select);

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Seleccionar...';
    defaultOption.selected = true;
    defaultOption.disabled = true;
    select.appendChild(defaultOption);

    items.forEach(item => {
        const opt = document.createElement('option');
        opt.value = item[valueKey];
        // Soporte para nombres compuestos (ej: first_name + last_name)
        if (textKey === 'full_name' && item.first_name) {
            opt.textContent = `${item.first_name} ${item.last_name || ''}`.trim();
        } else if (typeof textKey === 'function') {
            opt.textContent = textKey(item);
        } else {
            opt.textContent = item[textKey] || `#${item[valueKey]}`;
        }
        if (String(item[valueKey]) === targetVal) {
            opt.selected = true;
        }
        select.appendChild(opt);
    });

    // Inicializar Choices.js para búsqueda si está disponible
    if (typeof Choices !== 'undefined' && !select.dataset.choicesInitialized) {
        try {
            const choices = new Choices(select, {
                searchEnabled: true,
                itemSelectText: '',
                noResultsText: 'Sin resultados',
                noChoicesText: 'Sin opciones',
                shouldSort: false,
                searchPlaceholderValue: 'Buscar...',
            });
            select._choices = choices;
            select.dataset.choicesInitialized = 'true';
        } catch(e) {
        }
    }
}
