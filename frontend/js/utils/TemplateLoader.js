// Carga templates HTML de forma asíncrona con caché

export const TemplateLoader = {
    cache: {},

    // Carga un template desde una URL con fallback a ruta relativa
    async load(templateName) {
        if (this.cache[templateName]) {
            return this.cache[templateName];
        }

        const response = await fetch(`/templates/modals/${templateName}.html`);
        if (!response.ok) {
            const altResponse = await fetch(`templates/modals/${templateName}.html`);
            if (!altResponse.ok) throw new Error(`Template ${templateName} no encontrado`);
            const html = await altResponse.text();
            this.cache[templateName] = html;
            return html;
        }

        const html = await response.text();
        this.cache[templateName] = html;
        return html;
    }
};
