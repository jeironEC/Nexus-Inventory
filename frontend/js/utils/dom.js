// Utilidades para manipulación del DOM

// Crea un elemento con clases, atributos y hijos
export function create(tagName, classes = '', attrs = {}, children = null) {
    const element = document.createElement(tagName);
    const fullAttrs = { className: classes, ...attrs };

    Object.entries(fullAttrs).forEach(([key, value]) => {
        if (key === 'className') {
            element.className = value;
        } else if (key === 'dataset') {
            Object.entries(value).forEach(([dataKey, dataValue]) => {
                element.dataset[dataKey] = dataValue;
            });
        } else if (key.startsWith('on') && typeof value === 'function') {
            const event = key.slice(2).toLowerCase();
            element.addEventListener(event, value);
        } else if (key === 'style' && typeof value === 'object') {
            Object.assign(element.style, value);
        } else if (key === 'ref') {
            value.current = element;
        } else {
            element.setAttribute(key, value);
        }
    });

    if (children !== null) {
        if (Array.isArray(children)) {
            children.forEach(child => {
                if (typeof child === 'string') {
                    element.appendChild(document.createTextNode(child));
                } else if (child instanceof Node) {
                    element.appendChild(child);
                }
            });
        } else if (typeof children === 'string') {
            element.textContent = children;
        } else if (children instanceof Node) {
            element.appendChild(children);
        }
    }

    return element;
}

// Elimina todos los hijos de un elemento
export function clearChildren(element) {
    if (element.replaceChildren) {
        element.replaceChildren();
    } else {
        while (element.firstChild) {
            element.removeChild(element.firstChild);
        }
    }
}

// Convierte un string HTML en un DocumentFragment seguro
export function parseHTML(htmlString) {
    return document.createRange().createContextualFragment(htmlString);
}

// Reemplaza el contenido de un elemento con HTML
export function renderHTML(element, htmlString) {
    const fragment = parseHTML(htmlString);
    element.replaceChildren(fragment);
}
