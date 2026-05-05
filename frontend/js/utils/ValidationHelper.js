// Utilidades para validación de formularios

import { isValidEmail } from './helpers.js';

export const ValidationHelper = {
    // Valida un formulario completo
    validateForm(form) {
        let isValid = true;
        this.clearErrors(form);

        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            if (!this.validateInput(input)) {
                isValid = false;
            }
        });

        return isValid;
    },

    // Valida un campo individual
    validateInput(input) {
        const value = input.value.trim();
        const rules = input.dataset.validate ? input.dataset.validate.split(' ') : [];
        let error = null;

        // Validaciones nativas primero
        if (input.required && !value) {
            error = 'Este campo es obligatorio';
        } else if (input.type === 'email' && value && !isValidEmail(value)) {
            error = 'Formato de email inválido';
        } else if (input.minLength > 0 && value && value.length < input.minLength) {
            error = `Mínimo ${input.minLength} caracteres`;
        }

        // Validaciones personalizadas vía data-validate
        if (!error && value && rules.length > 0) {
            for (const rule of rules) {
                if (rule === 'number' && isNaN(value)) {
                    error = 'Debe ser un número';
                }
            }
        }

        if (error) {
            this.showError(input, error);
            return false;
        }

        return true;
    },

    // Muestra error en un campo
    showError(input, message) {
        input.classList.add('is-invalid');
        const parent = input.closest('.form-group') || input.parentElement;
        let errorEl = parent.querySelector('.error-message');

        if (!errorEl) {
            errorEl = document.createElement('div');
            errorEl.className = 'error-message';
            parent.appendChild(errorEl);
        }
        errorEl.textContent = message;
    },

    // Limpia errores del formulario
    clearErrors(form) {
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        form.querySelectorAll('.error-message').forEach(el => el.remove());
    },

    // Configura validación en tiempo real de contraseña
    setupPasswordValidation(passwordInput, requirementsContainer) {
        if (!passwordInput || !requirementsContainer) return;

        const reqs = {
            length: requirementsContainer.querySelector('#req-length'),
            upper: requirementsContainer.querySelector('#req-upper'),
            lower: requirementsContainer.querySelector('#req-lower'),
            number: requirementsContainer.querySelector('#req-number'),
            special: requirementsContainer.querySelector('#req-special')
        };

        // Mostrar el panel de requisitos cuando se hace focus
        passwordInput.addEventListener('focus', () => {
            requirementsContainer.style.display = 'grid';
        });

        // Validar cada tecla
        passwordInput.addEventListener('input', (e) => {
            const val = e.target.value;
            this.updateReqStatus(reqs.length, val.length >= 8);
            this.updateReqStatus(reqs.upper, /[A-Z]/.test(val));
            this.updateReqStatus(reqs.lower, /[a-z]/.test(val));
            this.updateReqStatus(reqs.number, /[0-9]/.test(val));
            this.updateReqStatus(reqs.special, /[!@#$%^&*(),.?":{}|<>]/.test(val));
        });
    },

    // Actualiza estado visual de requisito de contraseña
    updateReqStatus(reqElement, isValid) {
        if (!reqElement) return;
        const icon = reqElement.querySelector('.material-symbols-outlined');
        if (isValid) {
            reqElement.classList.add('valid');
            reqElement.classList.remove('invalid');
            if (icon) icon.textContent = 'check';
            reqElement.style.color = '#22c55e';
        } else {
            reqElement.classList.remove('valid');
            reqElement.classList.add('invalid');
            if (icon) icon.textContent = 'close';
            reqElement.style.color = 'var(--text-color-light, #94a3b8)';
        }
    },

    // Verifica si la contraseña cumple requisitos
    isPasswordValid(val) {
        if (!val) return false;
        return val.length >= 8 &&
               /[A-Z]/.test(val) &&
               /[a-z]/.test(val) &&
               /[0-9]/.test(val) &&
               /[!@#$%^&*(),.?":{}|<>]/.test(val);
    }
};
