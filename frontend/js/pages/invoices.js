// Lógica para la gestión y visualización de facturas

import { toast } from '../components/Toast.js';
import { serviceProvider } from '../services/ServiceProvider.js';
import { getFilterValues, initFilterListeners, loadFilterSelects } from '../utils/filter_utils.js';
import { DEFAULT_PAGINATION_LIMIT } from '../utils/const.js';
import { TablePagination } from '../components/Pagination.js';
import { formatDate, formatFullName, setButtonLoading } from '../utils/helpers.js';
import { Table } from '../components/Table.js';

let invoiceTable;

const TABLE_COLUMNS = [
    { label: 'ID', type: 'primary', value: (item) => `#${item.id}` },
    { label: 'Empresa', type: 'normal', value: (item) => item.company?.name || '-' },
    { label: 'N° Factura', type: 'primary', value: (item) => `<strong>${item.number_invoice || `#${item.id}`}</strong>` },
    { label: 'Tipo', type: 'normal', value: (item) => item.invoice_type === 'SALE' ? 'Venta' : 'Compra' },
    {
        label: 'Venta Asociada',
        type: 'normal',
        value: (item) => item.invoice_type === 'SALE'
            ? `Venta #${item.sale_id || (item.sale && item.sale.id) || 'N/A'}`
            : '-'
    },
    {
        label: 'Compra Asociada',
        type: 'normal',
        value: (item) => item.invoice_type === 'PURCHASE'
            ? `Compra #${item.purchase_id || (item.purchase && item.purchase.id) || 'N/A'}`
            : '-'
    },
    { label: 'PDF Generado', type: 'normal', value: (item) => item.pdf_generated ? 'Sí' : 'No' },
    { label: 'Estado', type: 'normal', value: (item) => `<span class="badge ${item.state === 'ISSUED' ? 'badge-success' : 'badge-danger'}">${item.state === 'ISSUED' ? 'Emitida' : 'Cancelada'}</span>` },
    { label: 'Creado en', type: 'normal', value: (item) => item.created_at ? formatDate(item.created_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Actualizado en', type: 'normal', value: (item) => item.updated_at ? formatDate(item.updated_at, 'dd/mm/yyyy HH:mm') : '-' },
    { label: 'Eliminado en', type: 'normal', value: (item) => item.deleted_at ? formatDate(item.deleted_at, 'dd/mm/yyyy HH:mm') : '-' }
];

// Inicializa la página de facturas
async function initInvoicesPage() {
    if (window.sidebar) {
        window.sidebar.init('invoices.html');
    }

    if (window.pageHeader) {
        window.pageHeader.init('Facturación');
    }

    invoiceTable = new Table({
        selector: '.table',
        columns: TABLE_COLUMNS,
        actions: {
            customHtml: (item) => `
                <div class="table-actions">
                    <button class="btn-action btn-download-pdf" title="Descargar PDF" data-invoice-id="${item.id}">
                        <span class="material-symbols-outlined">picture_as_pdf</span>
                    </button>
                    ${item.state === 'ISSUED' ? `
                    <button class="btn-action btn-action-danger btn-cancel-invoice" title="Anular Factura">
                        <span class="material-symbols-outlined">cancel</span>
                    </button>
                    ` : ''}
                </div>
            `,
            setupEvents: (tr, item) => {
                const btnDownloadPdf = tr.querySelector('.btn-download-pdf');
                if (btnDownloadPdf) {
                    btnDownloadPdf.addEventListener('click', (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        const invoiceNumber = item.number_invoice || item.id;
                        handleDownloadPdf(item.id, invoiceNumber, e.currentTarget);
                    });
                }

                const btnCancel = tr.querySelector('.btn-cancel-invoice');
                if (btnCancel) {
                    btnCancel.addEventListener('click', () => handleCancelInvoice(item));
                }
            }
        }
    });

    await loadFilterSelects([
        'invoice-filter-sale-id',
        'invoice-filter-purchase-id'
    ]);

    // Inicializar selects buscables en filtros
    import('../components/SearchableSelect.js').then(m => {
        m.SearchableSelect.initAll('.card-body');
    });

    await loadInvoicesData();

    initFilterListeners('.card', async () => {
        await loadInvoicesData();
    });
}

// Carga los datos de las facturas
async function loadInvoicesData() {
    invoiceTable.showLoading();

    try {
        const filters = {
            limit: 100,
            ...getFilterValues('.card')
        };

        const response = await serviceProvider.invoices.getAll(filters);
        if (response.success && response.data) {
            const items = response.data.results || (Array.isArray(response.data) ? response.data : []);

            const paginator = new TablePagination(items, DEFAULT_PAGINATION_LIMIT, (pagedData) => {
                invoiceTable.setData(pagedData);
            });

            paginator.init();
            invoiceTable.setData(paginator.getCurrentPageData());
        }
    } catch (error) {
        invoiceTable.showError('No se pudo cargar la información de facturas. ' + (error.message || ''));
    }
}

// Descarga el PDF de una factura
async function handleDownloadPdf(invoiceId, invoiceNumber, button) {
    let originalNodes = [];
    try {
        if (button) {
            originalNodes = setButtonLoading(button, true);
        }

        window.modal.showLoading('Información', 'Generando y descargando PDF...');

        const response = await serviceProvider.invoices.downloadPdf(invoiceId);

        if (response.success && response.data) {
            const blob = new Blob([response.data], { type: 'application/pdf' });

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `factura_${invoiceNumber}.pdf`;

            document.body.appendChild(a);
            a.click();

            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            window.modal.hideLoading();

            await loadInvoicesData();

            toast.show('PDF descargado correctamente', 'success');
        } else {
            throw new Error(response.message || 'No se pudo descargar el PDF');
        }
    } catch (error) {
        window.modal.hideLoading();
        window.modal.showAlert('Error', error.message || 'Error al descargar el PDF', 'error');

        if (button && originalNodes.length > 0) {
            setButtonLoading(button, false, originalNodes);
        }
    }
}

// Anula una factura
async function handleCancelInvoice(invoice) {
    window.modal.showConfirm(
        'Anular Factura',
        `¿Estás seguro de que deseas anular la factura ${invoice.number_invoice || '#'+invoice.id}? Esta operación es irreversible fiscalmente.`,
        async () => {
            try {
                const response = await serviceProvider.invoices.cancel(invoice.id);
                if (response.success) {
                    await loadInvoicesData();
                    toast.show('Factura anulada exitosamente', 'success');
                } else {
                    window.modal.showAlert('Error', response.message || 'No se pudo anular la factura', 'error');
                }
            } catch (error) {
                window.modal.showAlert('Error', error.message || 'Error al anular la factura', 'error');
            }
        }
    );
}

document.addEventListener('DOMContentLoaded', initInvoicesPage);
