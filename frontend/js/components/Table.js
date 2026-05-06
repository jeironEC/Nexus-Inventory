import { create, clearChildren, renderHTML } from '../utils/dom.js';
import { renderRow } from '../utils/base_page.js';
import { isAdmin } from '../utils/rbac.js';

// Encapsula lógica de renderizado de tablas con soporte para campos de auditoría

export class Table {
    // Constructor: configura el componente con selector, columnas, acciones y mensaje vacío
    constructor(config) {
        this.config = config;
        this.table = document.querySelector(config.selector);
        this.thead = this.table?.querySelector('thead');
        this.tbody = this.table?.querySelector('tbody');
        this.columns = config.columns || [];
        this.actions = config.actions || {};
        this.emptyMessage = config.emptyMessage || 'No se encontraron registros';

        if (!isAdmin()) {
            this.columns = this.columns.filter(col => col.type !== 'audit');
        }

        this.init();
    }

    // Inicializa la estructura de la tabla creando thead y tbody si no existen
    init() {
        if (!this.table) return;

        if (!this.thead) {
            this.thead = create('thead');
            this.table.appendChild(this.thead);
        }
        if (!this.tbody) {
            this.tbody = create('tbody');
            this.table.appendChild(this.tbody);
        }

        this.renderHeader();
    }

    // Genera el encabezado dinámicamente según las columnas configuradas
    renderHeader() {
        if (!this.thead) return;
        clearChildren(this.thead);

        const tr = create('tr');

        this.columns.forEach(col => {
            const className = `col-${col.type || 'normal'}`;
            const th = create('th', className, {}, col.label || '');
            tr.appendChild(th);
        });

        // Columna de acciones (siempre primaria)
        if (this.actions.onEdit || this.actions.onDelete || this.actions.onToggle || this.actions.customHtml) {
            const thActions = create('th', 'col-primary', {}, 'Acciones');
            tr.appendChild(thActions);
        }

        this.thead.appendChild(tr);
    }

    // Renderiza los datos en el cuerpo de la tabla
    setData(data) {
        if (!this.tbody) return;
        clearChildren(this.tbody);

        if (!data || data.length === 0) {
            const colCount = this.columns.length + (Object.keys(this.actions).length > 0 ? 1 : 0);
            renderHTML(this.tbody, `<tr><td colspan="${colCount}" class="text-center">${this.emptyMessage}</td></tr>`);
            return;
        }

        data.forEach(item => {
            renderRow(this.tbody, {
                item: item,
                columns: this.columns,
                actions: this.actions
            });
        });
    }

    // Muestra un indicador de carga en la tabla
    showLoading() {
        if (!this.tbody) return;
        const colCount = this.columns.length + (Object.keys(this.actions).length > 0 ? 1 : 0);
        clearChildren(this.tbody);
        renderHTML(this.tbody, `
            <tr>
                <td colspan="${colCount}" class="text-center" style="padding: 40px;">
                    <div class="spinner spinner-sm"></div>
                    <p style="margin-top: 10px; font-family: var(--font-mono); font-size: 11px; opacity: 0.5;">CARGANDO DATOS...</p>
                </td>
            </tr>
        `);
    }

    // Muestra un mensaje de error en la tabla
    showError(message) {
        if (!this.tbody) return;
        const colCount = this.columns.length + (Object.keys(this.actions).length > 0 ? 1 : 0);
        clearChildren(this.tbody);
        renderHTML(this.tbody, `
            <tr>
                <td colspan="${colCount}" class="text-center" style="padding: 30px; color: var(--danger);">
                    <span class="material-symbols-outlined" style="font-size: 32px; vertical-align: middle;">error</span>
                    <p style="margin-top: 10px; font-weight: 500;">${message || 'Error al cargar los datos'}</p>
                </td>
            </tr>
        `);
    }
}
