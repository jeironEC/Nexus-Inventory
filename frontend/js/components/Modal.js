import { parseHTML } from '../utils/dom.js';

// Gestiona la apertura, cierre y creación dinámica de modales en la aplicación

class Modal {
    constructor() {
        this.activeModal = null;
    }

    // Muestra un modal por su ID
    show(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        modal.classList.add('active');
        modal.classList.add('show');
        modal.style.display = 'flex';
        modal.style.opacity = '1';
        modal.style.visibility = 'visible';
        modal.style.zIndex = '9999';
        document.body.style.overflow = 'hidden';
        this.activeModal = modal;

        modal.querySelector('.modal-close')?.addEventListener('click', () => this.hide(modalId));
        modal.querySelector('.modal-cancel')?.addEventListener('click', () => this.hide(modalId));

        const backdrop = modal.querySelector('.modal-backdrop');
        if (backdrop) {
            backdrop.addEventListener('click', (e) => {
                if (e.target === backdrop) this.hide(modalId);
            });
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.activeModal) {
                this.hide(modalId);
            }
        });
    }

    // Oculta un modal por su ID y resetea su formulario si existe
    hide(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        modal.classList.remove('active');
        modal.classList.remove('show');
        modal.style.display = 'none';
        document.body.style.overflow = '';
        this.activeModal = null;

        const form = modal.querySelector('form');
        if (form) form.reset();
    }

    // Oculta todos los modales activos
    hideAll() {
        document.querySelectorAll('.modal-backdrop.active').forEach(backdrop => {
            backdrop.classList.remove('active');
            backdrop.style.display = 'none';
        });
        document.body.style.overflow = '';
        this.activeModal = null;
    }

    // Muestra un modal de alerta con título, mensaje y tipo
    showAlert(title, message, type = 'error', callback = null) {
        const modalId = 'modal-dynamic-alert';
        const modal = this._getDynamicModal(modalId, false);

        document.getElementById(`${modalId}-title`).textContent = title;
        document.getElementById(`${modalId}-msg`).textContent = message;

        const okBtn = document.getElementById(`${modalId}-ok`);
        const header = modal.querySelector('.modal-header');

        okBtn.style.display = 'block';

        if (type === 'error') {
            header.style.borderBottom = '3px solid var(--danger, #dc3545)';
        } else if (type === 'success') {
            header.style.borderBottom = '3px solid var(--success, #198754)';
        } else if (type === 'info' || type === 'warning') {
            header.style.borderBottom = '3px solid var(--primary, #0d6efd)';
        }

        okBtn.replaceWith(okBtn.cloneNode(true));
        const newOkBtn = document.getElementById(`${modalId}-ok`);
        newOkBtn.addEventListener('click', () => {
            this.hide(modalId);
            if (callback) callback();
        });

        this.show(modalId);
    }

    // Muestra un modal de carga con título y mensaje
    showLoading(title, message) {
        const modalId = 'modal-dynamic-alert';
        const modal = this._getDynamicModal(modalId, false);

        document.getElementById(`${modalId}-title`).textContent = title;
        document.getElementById(`${modalId}-msg`).textContent = message;

        const okBtn = document.getElementById(`${modalId}-ok`);
        const header = modal.querySelector('.modal-header');

        header.style.borderBottom = '3px solid var(--primary, #0d6efd)';

        // Ocultar botón durante carga
        okBtn.style.display = 'none';

        this.show(modalId);
    }

    // Oculta el modal de carga
    hideLoading() {
        this.hide('modal-dynamic-alert');
    }

    // Muestra un modal de confirmación con callback
    showConfirm(title, message, callback) {
        const modalId = 'modal-dynamic-confirm';
        const modal = this._getDynamicModal(modalId, true);

        document.getElementById(`${modalId}-title`).textContent = title;
        document.getElementById(`${modalId}-msg`).textContent = message;

        const okBtn = document.getElementById(`${modalId}-ok`);
        const cancelBtn = document.getElementById(`${modalId}-cancel`);

        // Asegurar que los botones sean visibles
        okBtn.style.display = 'block';
        if (cancelBtn) cancelBtn.style.display = 'block';

        okBtn.onclick = () => {
            this.hide(modalId);
            if (callback) callback();
        };

        cancelBtn.onclick = () => this.hide(modalId);
        this.show(modalId);
    }

    // Crea o reutiliza un modal dinámico
    _getDynamicModal(id, isConfirm = false) {
        let modal = document.getElementById(id);
        if (!modal) {
            modal = document.createElement('div');
            modal.className = 'modal-backdrop';
            modal.id = id;
            const cancelBtn = isConfirm
                ? `<button type="button" class="btn btn-secondary modal-cancel" id="${id}-cancel">Cancelar</button>`
                : '';

            const fragment = parseHTML(`
                <div class="modal" style="max-width: 420px;">
                    <div class="modal-header">
                        <h3 class="modal-title" id="${id}-title"></h3>
                        <button class="modal-close" aria-label="Cerrar">&times;</button>
                    </div>
                    <div class="modal-body">
                        <p id="${id}-msg" style="margin:0; font-size: 15px; color: rgba(206,232,242,0.85); line-height: 1.6;"></p>
                    </div>
                    <div class="modal-footer">
                        ${cancelBtn}
                        <button type="button" class="btn btn-primary" id="${id}-ok">Aceptar</button>
                    </div>
                </div>
            `);
            modal.appendChild(fragment);

            // Cerrar al hacer clic en el backdrop
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.hide(id);
            });
            document.body.appendChild(modal);
        }
        return modal;
    }
}

window.modal = new Modal();
export { Modal };
