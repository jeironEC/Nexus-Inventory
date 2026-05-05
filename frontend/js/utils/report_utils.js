// Utilidades para crear páginas de reporte con filtros y tablas

import { ReportHelper } from '../components/ReportHelper.js';
import { ReportTable } from '../components/ReportTable.js';

// Crea una página de reporte configurando filtros y tabla
export function createReportPage(config) {
    let reportTable;

    async function initReport() {
        const initialized = await ReportHelper.init({
            title: config.title,
            sidebarId: config.sidebarId,
            pdfEndpoint: config.pdfEndpoint,
            pdfFileName: config.pdfFileName
        });

        if (!initialized) return;

        if (config.onInit) {
            await config.onInit();
        }

        const btnApply = document.getElementById('btn-apply-filters');
        if (btnApply) {
            btnApply.addEventListener('click', () => loadReportData());
        }

        _addResetButton();
        await loadReportData();
    }

    function _addResetButton() {
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
            document.querySelectorAll('[id^="report-filter-"]').forEach(el => {
                if (el.tagName === 'SELECT') {
                    el.selectedIndex = 0;
                    if (el._choices) {
                        el._choices.removeActiveItems();
                        const firstVal = el.querySelector('option').value || '';
                        el._choices.setChoiceByValue(firstVal);
                    }
                } else {
                    el.value = '';
                }
            });
            loadReportData();
        });

        filterActions.appendChild(btnReset);
    }

    async function loadReportData() {
        const filters = ReportHelper.getFilters();
        reportTable.showLoading();

        try {
            const response = await config.serviceMethod(filters);

            if (response.success && response.data) {
                const data = response.data.data;

                if (config.onDataLoaded || config.processData) {
                    const processor = config.onDataLoaded || config.processData;
                    const result = processor(data, filters, config.columns);
                    if (result && result.data && result.columns) {
                        reportTable.renderHeader(result.columns);
                        reportTable.setData(result.data, result.columns);
                    }
                    return;
                }

                const viewKey = config.groupByField ? (filters[config.groupByField] || '') : null;

                if (config.groupByField && typeof config.columns === 'object' && !Array.isArray(config.columns)) {
                    const columns = config.columns[viewKey] || config.columns[Object.keys(config.columns)[0]];
                    let processedData = [];

                    if (!viewKey) {
                        if (data && !Array.isArray(data)) {
                            processedData = [data];
                        } else if (Array.isArray(data) && data.length > 0) {
                            processedData = data;
                        }
                    } else {
                        processedData = Array.isArray(data) ? data : [];
                    }

                    reportTable.renderHeader(columns);
                    reportTable.setData(processedData, columns);
                } else {
                    const processedData = Array.isArray(data) ? data : [];
                    reportTable.setData(processedData, config.columns);
                }
            } else {
                reportTable.showError(response.message || 'Error loading data');
            }
        } catch (error) {
            reportTable.showError(error.message || error.toString() || 'Error al cargar datos');
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        let defaultCols;
        if (typeof config.columns === 'object' && !Array.isArray(config.columns)) {
            defaultCols = config.columns[Object.keys(config.columns)[0]];
        } else {
            defaultCols = config.columns;
        }

        reportTable = new ReportTable({
            selector: '#report-table',
            defaultColumns: defaultCols,
            emptyMessage: 'No records available for selected filters'
        });

        initReport();
    });
}
