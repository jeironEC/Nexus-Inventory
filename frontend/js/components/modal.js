/**
 * MODAL.JS
 * Componente de modales globales.
 * Provee: showAlert() y showConfirm()
 *
 * Se usa desde page_header.js (confirmación logout)
 * y desde cualquier otra página que necesite alertas o confirmaciones.
 */

class Modal {
    constructor() {
        this.activeModal = null;
    }

    // ─── Muestra un modal existente en el DOM por ID ─────────────────
    show(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        modal.classList.add('active');
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        this.activeModal = modal;

        modal.querySelector('.modal-close')?.addEventListener('click', () => this.hide(modalId));
        modal.querySelector('.modal-cancel')?.addEventListener('click', () => this.hide(modalId));

        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.hide(modalId);
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.activeModal) this.hide(modalId);
        });
    }

    // ─── Oculta un modal por ID ───────────────────────────────────────
    hide(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        modal.classList.remove('active');
        modal.style.display = 'none';
        document.body.style.overflow = '';
        this.activeModal = null;

        const form = modal.querySelector('form');
        if (form) form.reset();
    }

    _getOrCreateModal(id, hasCancel) {
        let modal = document.getElementById(id);
        if (!modal) {
            // Backdrop
            modal = document.createElement('div');
            modal.className = 'modal-backdrop';
            modal.id = id;
            modal.style.display = 'none';

            // Modal box
            const modalBox = document.createElement('div');
            modalBox.className = 'modal';
            modalBox.style.maxWidth = '420px';

            // Header
            const header = document.createElement('div');
            header.className = 'modal-header';

            const title = document.createElement('h3');
            title.className = 'modal-title';
            title.id = `${id}-title`;

            const closeBtn = document.createElement('button');
            closeBtn.className = 'modal-close';
            closeBtn.setAttribute('aria-label', 'Cerrar');
            closeBtn.textContent = '×';

            header.appendChild(title);
            header.appendChild(closeBtn);

            // Body
            const body = document.createElement('div');
            body.className = 'modal-body';

            const msg = document.createElement('p');
            msg.id = `${id}-msg`;
            msg.style.cssText = 'margin:0; font-size:15px; color:rgba(206,232,242,0.85); line-height:1.6;';

            body.appendChild(msg);

            // Footer
            const footer = document.createElement('div');
            footer.className = 'modal-footer';

            if (hasCancel) {
                const cancelBtn = document.createElement('button');
                cancelBtn.type = 'button';
                cancelBtn.className = 'btn btn-secondary modal-cancel';
                cancelBtn.id = `${id}-cancel`;
                cancelBtn.textContent = 'Cancelar';
                footer.appendChild(cancelBtn);
            }

            const okBtn = document.createElement('button');
            okBtn.type = 'button';
            okBtn.className = 'btn btn-primary';
            okBtn.id = `${id}-ok`;
            okBtn.textContent = 'Aceptar';
            footer.appendChild(okBtn);

            // Ensamblar
            modalBox.appendChild(header);
            modalBox.appendChild(body);
            modalBox.appendChild(footer);
            modal.appendChild(modalBox);
            document.body.appendChild(modal);
        }
        return modal;
    }

    // ─── Alerta (solo OK) ────────────────────────────────────────────
    showAlert(title, message, type = 'error') {
        const id    = 'modal-dynamic-alert';
        const modal = this._getOrCreateModal(id, false);

        document.getElementById(`${id}-title`).textContent = title;
        document.getElementById(`${id}-msg`).textContent   = message;

        const header = modal.querySelector('.modal-header');
        if (type === 'error')   header.style.borderBottom = '3px solid var(--danger)';
        else if (type === 'success') header.style.borderBottom = '3px solid var(--success)';
        else                    header.style.borderBottom = '3px solid var(--sky)';

        document.getElementById(`${id}-ok`).onclick = () => this.hide(id);
        this.show(id);
    }

    // ─── Confirmación ───────────────────────────
    showConfirm(title, message, callback) {
        const id    = 'modal-dynamic-confirm';
        const modal = this._getOrCreateModal(id, true);

        document.getElementById(`${id}-title`).textContent = title;
        document.getElementById(`${id}-msg`).textContent   = message;

        document.getElementById(`${id}-ok`).onclick = () => {
            this.hide(id);
            if (callback) callback();
        };
        document.getElementById(`${id}-cancel`).onclick = () => this.hide(id);

        this.show(id);
    }
}

window.modal = new Modal();
