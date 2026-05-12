import { formatDate, formatFullName } from '../utils/helpers.js';
import { serviceProvider } from '../services/ServiceProvider.js';
import { create } from '../utils/dom.js';
import { getFilterValues, initFilterListeners, loadFilterSelects } from '../utils/filter_utils.js';
import { DEFAULT_PAGINATION_LIMIT } from '../utils/const.js';
import { TablePagination } from '../components/Pagination.js';
import { Table } from '../components/Table.js';
import { setupTableColumnToggles } from '../utils/base_page.js';

let movementTable;

// Inicializa los KPIs con valores por defecto
function initKpis() {
    const kpis = document.querySelectorAll('.card-kpi');

    if (kpis.length === 0) return;

    const defaults = [
        '0',
        '0\n(0 compras, 0 dev.)',
        '0\n(0 ventas, 0 dev.)',
        '+0'
    ];

    kpis.forEach((kpi, index) => {
        const valueEl = kpi.querySelector('.card-kpi-value');

        if (valueEl && defaults[index]) {
            const parts = defaults[index].split('\n');

            valueEl.innerHTML = `
                ${parts[0]}
                ${parts[1] ? `<div class="kpi-detail">${parts[1]}</div>` : ''}
            `;
        }
    });
}

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `#${item.id}` },
    { label: 'Producto', type: 'primary', value: (item) => item.product?.name || 'Desconocido' },
    { label: 'Categoría', type: 'normal', value: (item) => item.product?.category?.name || 'General' },
    {
        label: 'Tipo',
        type: 'normal',
        value: (item) => {
            const isIn = item.movement_type === 'IN';
            return `<span class="badge ${isIn ? 'badge-success' : 'badge-danger'}">${isIn ? 'Entrada' : 'Salida'}</span>`;
        }
    },
    {
        label: 'Origen',
        type: 'normal',
        value: (item) => {
            const sourceMap = {
                'COMPRA': 'Compra',
                'VENTA': 'Venta',
                'DEVOLUCION_VENTA': 'Devol. Venta',
                'DEVOLUCION_COMPRA': 'Devol. Compra',
                'MANUAL': 'Manual'
            };
            return sourceMap[item.source] || item.source || 'Desconocido';
        }
    },
    { label: 'Cantidad', type: 'normal', value: (item) => item.quantity },
    { label: 'Usuario', type: 'normal', value: (item) => item.user?.first_name ? formatFullName(item.user) : (item.user?.email || '-') },
    { label: 'Fecha', type: 'normal', value: (item) => item.created_at ? formatDate(item.created_at, 'dd/mm/yyyy HH:mm') : '-' }
];

// Inicializa la página
async function initInventoryMovementsPage() {
    if (window.sidebar) {
        window.sidebar.init('inventory_movements.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Movimientos de Inventario');
    }

    movementTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS
    });

    setupTableColumnToggles();

    await loadFilterSelects(['inventory-movement-filter-product-id', 'inventory-movement-filter-user-id']);

    import('../components/SearchableSelect.js').then(m => {
        m.SearchableSelect.initAll('.card-body');
    });

    initKpis();

    await loadMovementsData();

    initFilterListeners('.card', async () => {
        await loadMovementsData();
    });
}

// Carga los datos
async function loadMovementsData() {
    movementTable.showLoading();

    try {
        const filters = { limit: 100, ...getFilterValues('.card') };
        const response = await serviceProvider.inventoryMovements.getAll(filters);

        if (response.success && response.data) {
            const items = response.data.results || (Array.isArray(response.data) ? response.data : []);

            updateKpis(items);

            const paginator = new TablePagination(items, DEFAULT_PAGINATION_LIMIT, (pagedData) => {
                movementTable.setData(pagedData);
            });

            paginator.init();
            movementTable.setData(paginator.getCurrentPageData());
        }
    } catch (error) {
        movementTable.showError('No se pudo cargar el historial de movimientos. ' + (error.message || ''));
    }
}

// Actualiza los KPIs de la página
function updateKpis(items) {
    const kpis = document.querySelectorAll('.card-kpi');

    if (kpis.length === 0) return;

    let purchasesIn = 0;
    let saleReturnIn = 0;
    let salesOut = 0;
    let purchaseReturnOut = 0;

    items.forEach(item => {
        const qty = item.quantity || 0;
        const src = (item.source || '').toUpperCase();

        if (item.movement_type === 'IN') {
            if (src === 'COMPRA') {
                purchasesIn += qty;
            } else if (src === 'DEVOLUCION_VENTA') {
                saleReturnIn += qty;
            }
        } else {
            if (src === 'VENTA') {
                salesOut += qty;
            } else if (src === 'DEVOLUCION_COMPRA') {
                purchaseReturnOut += qty;
            }
        }
    });

    const totalEntries = purchasesIn + saleReturnIn;
    const totalExits = salesOut + purchaseReturnOut;
    const netQuantity = totalEntries - totalExits;

    const entriesBreakdown = `(${purchasesIn} compras, ${saleReturnIn} devoluciones)`;
    const exitsBreakdown = `(${salesOut} ventas, ${purchaseReturnOut} devoluciones)`;

    const values = [
        { value: items.length.toString(), detail: '' },
        { value: totalEntries.toString(), detail: entriesBreakdown },
        { value: totalExits.toString(), detail: exitsBreakdown },
        { value: `${netQuantity > 0 ? '+' : ''}${netQuantity}`, detail: '' }
    ];

    kpis.forEach((kpi, index) => {
        const valueEl = kpi.querySelector('.card-kpi-value');
        if (valueEl && values[index]) {
            valueEl.innerHTML = `
                ${values[index].value}
                ${values[index].detail ? `<div class="kpi-detail">${values[index].detail}</div>` : ''}
            `;
        }
    });
}

document.addEventListener('DOMContentLoaded', initInventoryMovementsPage);
