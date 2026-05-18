// Utilidades comunes para páginas CRUD

import { authService } from '../services/AuthService.js';
import { enforcePermission, applyDeclarativeRBAC, isAdmin } from './rbac.js';
import { create, clearChildren, parseHTML, renderHTML } from '../utils/dom.js';
import { getFilterValues, initFilterListeners } from './filter_utils.js';
import { DEFAULT_PAGINATION_LIMIT } from './const.js';
import { TablePagination } from '../components/Pagination.js';
import { fillForm, getFormData } from './form_utils.js';
import { TemplateLoader } from './TemplateLoader.js';
import { ValidationHelper } from './ValidationHelper.js';
import { toast } from '../components/Toast.js';
import { SearchableSelect } from '../components/SearchableSelect.js';

// Inicializa una página base con sidebar y header
export async function initPage(config) {
    const {
        pageName,
        htmlFile,
        filterSelectIds = [],
        onLoadData,
    } = config;

    // Verificar autenticación y permisos
    if (!authService.isAuthenticated()) {
        window.location.href = '/index.html';
        return;
    }

    enforcePermission(htmlFile);
    applyDeclarativeRBAC();
    setupTableColumnToggles();

    if (window.sidebar) {
        window.sidebar.init(htmlFile);
    }

    setupPageHeader(pageName, config.extraActions);

    for (const selectId of filterSelectIds) {
        const { loadFilterSelects } = await import('./filter_utils.js');
        await loadFilterSelects([selectId]);
    }

    if (onLoadData) {
        await onLoadData();
    }

    initFilterListeners('.card', onLoadData);

    // Inicializar selects buscables en filtros
    setTimeout(() => {
        SearchableSelect.initAll('.card-body');
    }, 200);
}

// Inicializa paginación y renderiza tabla
export function initTablePagination(data, pageSize, renderFn, paginationSelector) {
    const paginator = new TablePagination(data, pageSize, renderFn, paginationSelector);
    paginator.init();
    renderFn(paginator.getCurrentPageData());
    return paginator;
}

// Crea botón para nuevo registro
export function createNewButton(btnId, label, onClick) {
    const btnNew = create('button', 'btn btn-primary', { id: btnId });
    btnNew.appendChild(create('span', 'material-symbols-outlined', {}, 'add'));
    btnNew.appendChild(document.createTextNode(label));
    btnNew.addEventListener('click', onClick);
    return btnNew;
}

// Carga datos del servicio con filtros
export async function loadData(config) {
    const { service, renderFn, limit = DEFAULT_PAGINATION_LIMIT } = config;

    // Mostrar spinner mientras cargan los datos
    const tbody = document.querySelector('.table tbody');
    if (tbody) {
        clearChildren(tbody);
        renderHTML(tbody, `
            <tr>
                <td colspan="20" style="text-align: center; padding: 40px 0;">
                    <div style="display: flex; flex-direction: column; align-items: center; gap: 12px;">
                        <div class="spinner spinner-sm"></div>
                        <span style="font-family: var(--font-mono); font-size: 11px; color: rgba(206, 232, 242, 0.4); letter-spacing: 0.1em; text-transform: uppercase;">Cargando datos...</span>
                    </div>
                </td>
            </tr>
        `);
    }

    try {
        const filters = {
            limit,
            ...getFilterValues('.card')
        };

        const response = await service.getAll(filters);
        if (response.success && response.data) {
            const items = response.data.results || (Array.isArray(response.data) ? response.data : []);

            const paginator = new TablePagination(items, limit, (pagedData) => {
                renderFn(pagedData);
            });

            paginator.init();
            renderFn(paginator.getCurrentPageData());
        } else {
            toast.show(response.message || 'Error al cargar datos', 'error');
            renderFn([]);
        }
    } catch (error) {
         toast.show('No se pudieron cargar los datos. ' + (error.message || ''), 'error');
    }
}

// Alterna estado activo/inactivo de un registro
export async function handleToggle(config) {
    const { item, service, loadFn, singularName } = config;
    const isActive = item.is_active;
    const action = isActive ? 'desactivar' : 'activar';
    const name = item.name || item.first_name || item.title || `#${item.id}`;
    window.modal.showConfirm(
        'Confirmar acción',
        `¿Estás seguro de que deseas ${action} el ${singularName} "${name}"?`,
        async () => {
            try {
                const response = isActive
                    ? await service.deactivate(item.id)
                    : await service.activate(item.id);

                if (response.success) {
                    toast.show(`${singularName} ${action === 'activar' ? 'activado' : 'desactivado'} correctamente`, 'success');
                    if (loadFn) await loadFn();
                } else {
                    window.modal.showAlert('Error', response.message || `No se pudo ${action} el ${singularName}`, 'error');
                }
            } catch (error) {
                window.modal.showAlert('Error', error.message || `Error al ${action} el ${singularName}`, 'error');
            }
        }
    );
}

// Muestra modal para crear o editar
export async function showModal(config) {
    const { template, modalId, formId, item, onShow, onSubmit } = config;

    if (!window.modal) return;

    const existingModal = document.getElementById(modalId);
    if (existingModal) existingModal.remove();

    // Cargar template de forma asíncrona
    const templateHtml = await TemplateLoader.load(template);

    const container = create('div');
    const templateFragment = parseHTML(templateHtml);
    container.appendChild(templateFragment);
    const modalNode = container.firstElementChild;
    document.body.appendChild(modalNode);

    const isEdit = !!item;
    const titleEl = modalNode.querySelector('.modal-title');
    const submitBtn = modalNode.querySelector('button[type="submit"]');
    const form = document.getElementById(formId);

    if (isEdit) {
        titleEl.textContent = `Editar ${config.singularName}`;
        submitBtn.textContent = 'Guardar Cambios';
        if (form) {
            fillForm(form, item);
            form.dataset.id = item.id;
        }
    } else {
        titleEl.textContent = `Nuevo ${config.singularName}`;
        submitBtn.textContent = `Crear ${config.singularName}`;
    }

    window.modal.show(modalId);

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            onSubmit(e, form);
        });
    }

    if (onShow) {
        await onShow(form, item);
    }

    // Inicializar selects buscables en el modal (después de que onShow haya poblado los selects)
    setTimeout(() => {
        SearchableSelect.initAll(modalNode);
    }, 200);
}

// Maneja el envío del formulario
export async function handleSubmit(e, config) {
    const { service, modalId, loadFn, singularName, customData } = config;
    const form = e.target || e;

    // Validar formulario
    if (!customData && !ValidationHelper.validateForm(form)) {
        return;
    }

    const id = form.dataset.id;
    const data = customData || getFormData(form);

    try {
        const response = id
            ? await service.update(id, data)
            : await service.create(data);

        if (response.success) {
            toast.show(`${singularName} ${id ? 'actualizado' : 'creado'} correctamente`, 'success');
            window.modal.hide(modalId);
            const modalEl = document.getElementById(modalId);
            if (modalEl) modalEl.remove();

            if (loadFn) await loadFn();
        } else {
            window.modal.showAlert('Atención', response.message || `Error al procesar ${singularName}`, 'error');
        }
    } catch (error) {
        window.modal.showAlert('Atención', error.message || `Error al procesar ${singularName}`, 'error');
    }
}

// Renderiza una fila de tabla
export function renderRow(tbody, config) {
    const { item, columns, actions } = config;
    const tr = document.createElement('tr');
    const isActive = item.is_active;

    // Renderizar columnas de datos
    columns.forEach(col => {
        const td = document.createElement('td');
        const type = col.type || 'normal';
        td.className = `col-${type}`;

        const val = col.value(item);
        if (typeof val === 'string' && (val.includes('<') || val.includes('>'))) {
            td.appendChild(parseHTML(val || '-'));
        } else {
            td.textContent = val || '-';
        }
        tr.appendChild(td);
    });

    if (actions?.onEdit || actions?.onToggle || actions?.onDelete || actions?.customHtml) {
        const actionsTd = document.createElement('td');

        if (actions?.customHtml) {
            actionsTd.appendChild(parseHTML(actions.customHtml(item) || ''));
            tr.appendChild(actionsTd);
            if (actions?.setupEvents) {
                actions.setupEvents(tr, item);
            }
        } else {
            const actionsHtml = `
                <div class="table-actions">
                    ${actions.onEdit ? `<button class="btn-action btn-edit" title="Editar">
                        <span class="material-symbols-outlined">edit</span>
                    </button>` : ''}
                    ${actions.onToggle ? `<button class="btn-action btn-toggle ${isActive ? 'btn-action-danger' : ''}" title="${isActive ? 'Desactivar' : 'Activar'}">
                        <span class="material-symbols-outlined">${isActive ? 'block' : 'check_circle'}</span>
                    </button>` : ''}
                </div>
            `;
            actionsTd.appendChild(parseHTML(actionsHtml));
            tr.appendChild(actionsTd);

            if (actions?.onEdit) {
                const btnEdit = tr.querySelector('.btn-edit');
                if (btnEdit) btnEdit.addEventListener('click', () => actions.onEdit(item));
            }
            if (actions?.onToggle) {
                const btnToggle = tr.querySelector('.btn-toggle');
                if (btnToggle) btnToggle.addEventListener('click', () => actions.onToggle(item));
            }
        }
    }

    tbody.appendChild(tr);
}

// Configura botones para alternar vista de tabla
export function setupTableColumnToggles() {
    const container = document.querySelector('.table-container');
    const table = document.querySelector('.table');
    if (!container || !table || !isAdmin()) return;

    if (document.querySelector('.table-view-toggles')) return;

    // Verificar si la tabla tiene columnas de auditoría
    const hasAuditColumns = table.querySelector('.col-audit') ||
        table.querySelector('thead th.col-audit') ||
        table.querySelectorAll('thead th').length > 0 &&
        [...table.querySelectorAll('thead th')].some(th => th.classList.contains('col-audit'));

    if (!hasAuditColumns) return;

    table.classList.add('view-normal');

    const toggleWrapper = document.createElement('div');
    toggleWrapper.className = 'table-view-toggles';
    toggleWrapper.innerHTML = `
        <button class="btn btn-view-normal active">Campos Normales</button>
        <button class="btn btn-view-audit">Campos de Auditoría</button>
    `;

    container.parentNode.insertBefore(toggleWrapper, container);

    const btnNormal = toggleWrapper.querySelector('.btn-view-normal');
    const btnAudit = toggleWrapper.querySelector('.btn-view-audit');

    btnNormal.addEventListener('click', () => {
        table.classList.remove('view-audit');
        table.classList.add('view-normal');
        btnNormal.classList.add('active');
        btnAudit.classList.remove('active');
    });

    btnAudit.addEventListener('click', () => {
        table.classList.remove('view-normal');
        table.classList.add('view-audit');
        btnAudit.classList.add('active');
        btnNormal.classList.remove('active');
    });
}

// Configura el header de la página (uso interno)
function setupPageHeader(pageName, extraActions) {
    if (!window.pageHeader) return;

    if (extraActions) {
        window.pageHeader.init(pageName, { extraActions });
    } else {
        window.pageHeader.init(pageName);
    }
}
