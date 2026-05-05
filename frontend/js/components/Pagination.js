import { clearChildren, create } from '../utils/dom.js';

// Gestiona la paginación del lado del cliente con controles de navegación

export class TablePagination {
    // Constructor: configura paginación con datos, tamaño de página y callback de renderizado
    constructor(data, pageSize = 25, renderCallback, containerSelector = '.pagination') {
        this.data = data || [];
        this.pageSize = pageSize;
        this.currentPage = 1;
        this.renderCallback = renderCallback;
        this.container = document.querySelector(containerSelector);
    }

    get totalPages() {
        const total = Math.ceil(this.data.length / this.pageSize);
        return total > 0 ? total : 1;
    }

    // Obtiene los datos correspondientes a la página actual
    getCurrentPageData() {
        const start = (this.currentPage - 1) * this.pageSize;
        const end = start + this.pageSize;
        return this.data.slice(start, end);
    }

    // Inicializa los controles de paginación en el DOM
    init() {
        if (!this.container) {
            return;
        }
        this.updateUI();
    }

    // Navega a una página específica y actualiza la vista
    goToPage(page) {
        if (page < 1 || page > this.totalPages) return;
        this.currentPage = page;
        this.updateUI();
        if (this.renderCallback) {
            this.renderCallback(this.getCurrentPageData());
        }
    }

    // Actualiza los controles de paginación y genera botones dinámicos
    updateUI() {
        if (!this.container) return;

        // 1. Actualizar texto informativo
        const info = this.container.querySelector('.pagination-info');
        if (info) {
            const start = this.data.length === 0 ? 0 : (this.currentPage - 1) * this.pageSize + 1;
            const end = Math.min(this.currentPage * this.pageSize, this.data.length);
            info.textContent = `Mostrando ${start}-${end} de ${this.data.length} registros`;
        }

        // 2. Limpiar botones de números existentes para regenerarlos
        const numberButtons = this.container.querySelectorAll('.pagination-btn:not([aria-label])');
        numberButtons.forEach(btn => btn.remove());

        const nextBtn = this.container.querySelector('button[aria-label="Página siguiente"]');
        const prevBtn = this.container.querySelector('button[aria-label="Página anterior"]');

        // 3. Configurar botones de navegación (flechas)
        if (prevBtn) {
            prevBtn.disabled = this.currentPage === 1 || this.data.length === 0;
            prevBtn.onclick = () => this.goToPage(this.currentPage - 1);
        }

        if (nextBtn) {
            nextBtn.disabled = this.currentPage === this.totalPages || this.data.length === 0;
            nextBtn.onclick = () => this.goToPage(this.currentPage + 1);
        }

        // 4. Generar botones de números dinámicos
        const maxVisible = 5;
        let start = Math.max(1, this.currentPage - 2);
        let end = Math.min(this.totalPages, start + maxVisible - 1);

        if (end - start < maxVisible - 1) {
            start = Math.max(1, end - maxVisible + 1);
        }

        for (let i = start; i <= end; i++) {
            const btn = create('button', `pagination-btn ${i === this.currentPage ? 'active' : ''}`, {}, i.toString());
            btn.onclick = () => this.goToPage(i);
            if (nextBtn) {
                this.container.insertBefore(btn, nextBtn);
            } else {
                this.container.appendChild(btn);
            }
        }
    }
}
