"use strict";
(function () {
    const setUp = () => {

        const allPanels: NodeListOf<HTMLElement> = document.querySelectorAll('[data-target]');

        const hidePanel = (element: HTMLElement) => {
            const panelSelector = element.dataset.target || "";
            if (panelSelector !== "") {
                const panel = document.querySelector(panelSelector);
                if (panel !== null) {
                    panel.classList.add('hidden');
                    element.classList.remove("active");
                }
            }
        }

        const showPanel = (event: Event) => {
            const element = event.target as HTMLElement | null;
            if (element !== null) {
                const panelSelector = element.dataset.target || "";
                if (panelSelector !== "") {
                    const panel = document.querySelector(panelSelector);
                    if (panel !== null) {
                        allPanels.forEach(hidePanel);
                        panel.classList.remove('hidden');
                        element.classList.add("active");
                    }
                }
            }
        }

        allPanels.forEach((value) => {
            value.addEventListener("click", showPanel);
        });
    };
    if (document.readyState !== 'loading') {
        console.debug("ready");
        return setUp();
    }
    else {
        return document.addEventListener('DOMContentLoaded', setUp);
    }
})();
//# sourceMappingURL=init.js.map
