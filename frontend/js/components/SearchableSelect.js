// Inicializa selects buscables utilizando Choices.js

export class SearchableSelect {
    // Opciones por defecto para Choices.js
    static get defaultOptions() {
        return {
            searchEnabled: true,
            itemSelectText: 'Seleccionar',
            noResultsText: 'No se encontraron resultados',
            noChoicesText: 'No hay opciones disponibles',
            placeholder: false,
            shouldSort: false
        };
    }

    // Inicializa Choices.js en todos los selects del contenedor especificado
    static initAll(container = document, options = {}) {
        const root = typeof container === 'string' ? document.querySelector(container) : container;
        if (!root) return [];

        const selects = root.querySelectorAll('select:not(.no-choices)');
        const instances = [];

        selects.forEach(select => {
            const instance = this.init(select, options);
            if (instance) instances.push(instance);
        });

        return instances;
    }

    // Inicializa Choices.js en un select específico evitando duplicados
    static init(element, options = {}) {
        const el = typeof element === 'string' ? document.querySelector(element) : element;
        if (!el || el.dataset.choicesInitialized) return null;

        try {
            if (typeof Choices !== 'undefined') {
                const choices = new Choices(el, { ...this.defaultOptions, ...options });
                el.dataset.choicesInitialized = 'true';
                el._choices = choices;
                return choices;
            }
        } catch (e) {
        }
        return null;
    }
}
