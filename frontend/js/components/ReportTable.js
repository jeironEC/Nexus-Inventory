import { create, clearChildren, renderHTML } from '../utils/dom.js';
import { TablePagination } from './Pagination.js';

// Maneja tablas de reportes con columnas dinámicas y paginación

export class ReportTable {
    // Constructor: configura la tabla con selector, columnas y mensaje vacío
    constructor(config) {
        this.config = config;
        this.table = document.querySelector(config.selector);
        this.thead = this.table?.querySelector('thead');
        this.tbody = this.table?.querySelector('tbody');

        this.defaultColumns = config.defaultColumns || [];
        this.emptyMessage = config.emptyMessage || 'No hay registros disponibles';
        this.paginationContainer = document.querySelector(config.paginationSelector || '.pagination');
        this.paginationSelector = config.paginationSelector || '.pagination';

        this.allData = [];
        this.currentColumns = this.defaultColumns;
        this.paginator = null;

        this.init();
    }

    // Inicializa la estructura de la tabla creando thead y tbody si no existen
    init() {
        if (!this.table) return;

        if (!this.thead) {
            this.thead = document.createElement('thead');
            this.thead.id = 'report-table-header';
            this.table.appendChild(this.thead);
        }

        if (!this.tbody) {
            this.tbody = document.createElement('tbody');
            this.tbody.id = 'report-table-body';
            this.table.appendChild(this.tbody);
        }

        this.renderHeader(this.defaultColumns);
    }

    // Renderiza el encabezado de la tabla con las columnas especificadas
    renderHeader(columns) {
        if (!this.thead) return;
        clearChildren(this.thead);
        this.currentColumns = columns;

        const tr = document.createElement('tr');

        columns.forEach(col => {
            const th = create('th', 'col-normal', {}, col.label || '');
            tr.appendChild(th);
        });

        this.thead.appendChild(tr);
    }

    // Renderiza los datos en la tabla y configura la paginación
    setData(data, columns = null) {
        if (!this.tbody) return;
        clearChildren(this.tbody);

        const colsToUse = columns || this.defaultColumns;
        this.allData = data || [];

        if (!this.allData.length) {
            const colCount = colsToUse.length;
            renderHTML(this.tbody, `
                <tr>
                    <td colspan="${colCount}" class="text-center text-muted" style="padding:40px 20px;">
                        ${this.emptyMessage}
                    </td>
                </tr>
            `);
            if (this.paginationContainer) {
                this._updatePaginationInfo(0, 0, 0);
            }
            return;
        }

        this.paginator = new TablePagination(this.allData, 25, (pageData) => {
            this._renderRows(pageData, colsToUse);
        }, this.paginationSelector);

        if (this.paginationContainer) {
            this.paginator.init();
        }

        this.paginator.goToPage(1);
    }

    // Renderiza las filas de la tabla con los datos proporcionados
    _renderRows(items, columns) {
        if (!this.tbody) return;
        clearChildren(this.tbody);

        items.forEach(item => {
            const tr = document.createElement('tr');

            columns.forEach(col => {
                let content = col.value(item);
                const td = create('td', 'col-normal', {});

                if (content instanceof HTMLElement) {
                    td.appendChild(content);
                } else {
                    td.textContent = content !== undefined && content !== null ? content.toString() : '-';
                }

                tr.appendChild(td);
            });

            this.tbody.appendChild(tr);
        });
    }

    // Actualiza el texto informativo de la paginación
    _updatePaginationInfo(start, end, total) {
        const info = this.paginationContainer?.querySelector('.pagination-info');
        if (info) {
            info.textContent = total > 0 ? `Mostrando ${start}-${end} de ${total} registros` : 'Sin registros';
        }
    }

    // Muestra un indicador de carga en la tabla
    showLoading(colSpan = 5) {
        if (!this.tbody) return;
        clearChildren(this.tbody);
        renderHTML(this.tbody, `
            <tr>
                <td colspan="${colSpan}" style="text-align:center;padding:40px 0;">
                    <div style="display:flex;flex-direction:column;align-items:center;gap:12px;">
                        <div class="spinner spinner-sm"></div>
                        <span style="font-family:var(--font-mono);font-size:11px;color:rgba(206,232,242,0.4);letter-spacing:0.1em;text-transform:uppercase;">Cargando datos...</span>
                    </div>
                </td>
            </tr>
        `);
    }

    // Muestra un mensaje de error en la tabla
    showError(message, colSpan = 5) {
        if (!this.tbody) return;
        clearChildren(this.tbody);
        renderHTML(this.tbody, `
            <tr>
                <td colspan="${colSpan}" class="text-center text-danger" style="padding:40px 20px;font-weight:bold;">
                    Error: ${message || 'Error al cargar datos'}
                </td>
            </tr>
        `);
    }
}
