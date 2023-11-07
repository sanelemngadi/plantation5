"use strict";
console.log("Hello world");
class PlantationAccordion {
    constructor(_elements) {
        this._elements = _elements;
        this.bindAccordions();
    }
    bindAccordions() {
        for (const accordion of this._elements) {
            const header = this.$(accordion, '.plantation-options_header');
            if (!header)
                continue;
            header.addEventListener("mouseup", () => {
                accordion.classList.toggle('plantation-active');
            });
        }
    }
    $(element, selector) {
        return element.querySelector(selector);
    }
}
const accordions = Array.from(document.querySelectorAll('.plantation-options_item'));
new PlantationAccordion(accordions);
class PlantationNotebook {
    constructor(_element) {
        this._element = _element;
        this.bindNotebook();
    }
    bindNotebook() {
        // const header = this.$(notebook, '.plantation-options_header');
        const tabs = this._element.querySelector(".plantation-notebook_tabs");
        if (!tabs)
            return;
        Array.from(tabs.children).forEach(element => {
            element.addEventListener("mousedown", () => {
                this.setActiveItem(element);
            });
        });
    }
    setActiveItem(active) {
        const tabs = this._element.querySelector(".plantation-notebook_tabs");
        if (!tabs)
            return;
        let former_active = null;
        const cls = "plantation-active";
        const children = Array.from(tabs.children);
        children.forEach(child => {
            if (child.classList.contains(cls)) {
                former_active = child;
                child.classList.remove(cls);
            }
        });
        if (active) {
            if (!active.classList.contains(cls)) {
                active.classList.add(cls);
            }
        }
        if (former_active !== active) {
            if (active) {
                // const bodyItem = 
                const href = active.getAttribute("href");
                // active.classList.toggle(cls);
                // active.classList
                const activeBody = document.querySelector(href || "");
                if (activeBody) {
                    this.closePanes();
                    activeBody.classList.add(cls);
                }
                console.log("yes");
            }
        }
    }
    $(element, selector) {
        return element.querySelector(selector);
    }
    closePanes() {
        const panes = this._element.querySelector(".plantation-notebook_body");
        if (!panes)
            return;
        const cls = "plantation-active";
        const children = Array.from(panes.children);
        children.forEach(child => {
            if (child.classList.contains(cls)) {
                child.classList.remove(cls);
            }
        });
    }
}
const notebooks = Array.from(document.querySelectorAll('.plantation-notebook'));
notebooks.forEach(nb => {
    new PlantationNotebook(nb);
});
