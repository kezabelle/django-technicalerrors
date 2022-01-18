;(function () {
    "use strict";
    const setUp = () => {

        const allPanels: NodeListOf<HTMLElement> = document.querySelectorAll('[data-tab-target]');
        const allToggles: NodeListOf<HTMLElement> = document.querySelectorAll('[data-toggle-target]');

        const hidePanel = (element: HTMLElement) => {
            const panelSelector = element.dataset.tabTarget || "";
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
                const panelSelector = element.dataset.tabTarget || "";
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

        const toggleRelated = (event: Event) => {
            const element = event.target as HTMLElement | null;
            if (element !== null) {
                const toggleSelector = element.dataset.toggleTarget || "";
                if (toggleSelector !== "") {
                    const panel = document.querySelector(toggleSelector);
                    if (panel !== null) {
                        if (panel.classList.contains("hidden")) {
                            panel.classList.remove('hidden');
                        } else {
                            panel.classList.add('hidden');
                        }
                        element.classList.add("active");
                    }
                }
            }
        }

        class Tooltip {
            private owner: HTMLElement;
            public template: HTMLElement;
            private open: boolean;

            constructor(element: HTMLElement, template: string = '<div class="tooltip2" role="tooltip" aria-hidden="true"></div>') {
                this.owner = element;
                const parsedTemplate = new DOMParser().parseFromString(template, 'text/html').body.firstElementChild as HTMLElement | null;
                if (parsedTemplate === null) {
                    throw new Error("No HTML parsed")
                }
                this.template = parsedTemplate;
                this.open = false;
                this.show = this.show.bind(this);
                this.hide = this.hide.bind(this);
                this.maybeHide = this.maybeHide.bind(this);
                this.bind();
            }

            static ready(selector: string) {
                const foundTips: NodeListOf<HTMLElement> = document.querySelectorAll(selector);
                return foundTips.forEach((value) => {
                    return new Tooltip(value);
                });
            }

            bind() {
                this.owner.addEventListener("touchstart", this.show);
                this.owner.addEventListener("mouseenter", this.show);
            }

            unbind() {
                this.owner.removeEventListener("touchstart", this.show);
                this.owner.removeEventListener("mouseenter", this.show);
                this.owner.removeEventListener("mouseleave", this.hide);
            }

            show(event: MouseEvent | PointerEvent | TouchEvent) {
                if (!this.open) {
                    event.stopPropagation();

                    // Remove opportunities to try and show this again WHILE it is open.
                    this.owner.removeEventListener("touchstart", this.show);
                    this.owner.removeEventListener("mouseenter", this.show);

                    // Set up the listeners to handle removing this
                    this.owner.addEventListener("mouseleave", this.hide);
                    document.addEventListener("touchstart", this.maybeHide);
                    document.addEventListener("scroll", this.maybeHide);
                    document.addEventListener("keydown", this.maybeHide);

                    const {x, y, height, width} = this.owner.getBoundingClientRect();
                    console.log('show', event);

                    const yTether = (y + height + (height / 2)).toFixed(0);
                    const xTether = (x + (width / 2)).toFixed(0);
                    this.template.textContent = this.owner.getAttribute("aria-label");
                    this.template.style.top = `${yTether}px`;
                    this.template.style.left = `${xTether}px`;

                    this.owner.dataset.tooltipIsOpen = 'true';
                    this.owner.classList.add("tooltip-open");
                    document.body.appendChild(this.template);

                    // Await any animations which run on DOM node creation
                    Promise.allSettled(this.template.getAnimations().map(
                        (animation) => animation.finished
                    )).then(() => {
                        this.template.classList.add("open");

                        // Await any animations which run on entering.
                        Promise.allSettled(this.template.getAnimations().map(
                            (animation) => animation.finished
                        )).then(() => {
                            this.open = true;
                        });

                    });
                }
            }

            hide(event: MouseEvent | PointerEvent | Event) {
                if (this.open) {
                    console.log('hide', event);

                    // Remove opportunities to try and hide this again WHILE it is hidden.
                    this.owner.removeEventListener("mouseleave", this.hide);
                    document.removeEventListener("touchstart", this.maybeHide);
                    document.removeEventListener("scroll", this.maybeHide);
                    document.removeEventListener("keydown", this.maybeHide);

                    // Set up the listeners to handle showing this again subsequently.
                    this.owner.addEventListener("touchstart", this.show);
                    this.owner.addEventListener("mouseenter", this.show);

                    this.owner.classList.remove("tooltip-open");
                    this.owner.dataset.tooltipIsOpen = 'false';

                    this.template.classList.remove("open");

                    // Await any animations which occur when open is removed and it's leaving
                    Promise.allSettled(this.template.getAnimations().map(
                        (animation) => animation.finished
                    )).then(() => {
                        document.body.removeChild(this.template);
                        this.open = false;
                    });

                }
            }

            maybeHide(event: MouseEvent | PointerEvent | KeyboardEvent | Event) {
                if (this.open) {
                    console.log('maybe hide', event);
                    if (event.type === 'scroll') {
                        return this.hide(event);
                    } else if (event.type === 'keydown' && (event as KeyboardEvent).key === "Escape") {
                        // Pressing escape should hide the tooltip for Accessibility reasons.
                        // Stop the propagation to prevent this having any other consequences.
                        event.stopPropagation();
                        return this.hide(event);
                    } else if (event.target !== this.owner) {
                        return this.hide(event);
                    }
                }
            }
        }

        class Traceback {
            private owner: HTMLElement;

            constructor(element: HTMLElement) {
                this.owner = element;
                this.show = this.show.bind(this);
                this.hide = this.hide.bind(this);
                this.toggle = this.toggle.bind(this);
                this.bind();
            }

            bind() {
                this.owner.addEventListener("click", this.toggle);
            }

            static ready(selector: string) {
                const foundTraces: NodeListOf<HTMLElement> = document.querySelectorAll(selector);
                return foundTraces.forEach((value) => {
                    return new Traceback(value);
                });
            }

            toggle(event: MouseEvent | PointerEvent) {
                if (this.owner.classList.contains('active')) {
                    return this.hide(event);
                }
                return this.show(event);
            }

            hide(event: MouseEvent | PointerEvent) {
                this.owner.classList.remove('active');
            }

            show(event: MouseEvent | PointerEvent) {
                this.owner.classList.add('active');
                const {x, y, top} = this.owner.getBoundingClientRect();
                const {scrollX, scrollY} = window;
                const goTo = scrollY + top;
                // if (goTo > scrollY) {
                // TODO: detect reduced motion and make this not happen then!
                window.scroll({
                    top: goTo,
                    behavior: 'smooth'
                });
                // } else {
                //     window.scrollTo(scrollX, scrollY);
                // }
                // const silencedChildren: NodeListOf<HTMLElement> = this.owner.querySelectorAll('.traceback-locals, .traceback-context');
                // silencedChildren.forEach((value) => {
                //     value.classList.remove('hidden');
                // });
                // const contextLine: HTMLElement | null = this.owner.querySelector('.active');
                // if (contextLine) {
                //     contextLine.classList.add('bg-red-500');
                //     contextLine.classList.add('text-white')
                // }
            }
        }


        allPanels.forEach((value) => {
            value.addEventListener("click", showPanel);
        });
        allToggles.forEach((value) => {
            value.addEventListener("click", toggleRelated);
        });


        const initialTab = document.location.hash;
        if (initialTab !== '') {
            allPanels.forEach((value) => {
                if (value.dataset.tabTarget === initialTab) {
                    value.click();
                }
            });
        }

        Tooltip.ready('[data-tooltip-target]');
        Traceback.ready('[data-traceback]');

        const copyToClipboardButton = document.querySelector('.traceback-clipboard') as HTMLButtonElement | null;
        const copyToClipboardContents = document.getElementById("traceback_area") as HTMLTextAreaElement | null ;
        if (copyToClipboardButton !== null && copyToClipboardContents !== null) {
            const originalText = copyToClipboardButton.textContent;
            copyToClipboardButton.addEventListener('click', () => {
                navigator.clipboard.writeText(copyToClipboardContents.value).then(function () {
                    copyToClipboardButton.textContent = "Copied!"
                    setTimeout(() => {
                        copyToClipboardButton.textContent = originalText;
                    }, 1000);
                }, function () {
                    copyToClipboardButton.textContent = "Failed to copy";
                    setTimeout(() => {
                        copyToClipboardButton.textContent = originalText;
                    }, 1000);
                });
            });
        }
    };
    if (document.readyState !== 'loading') {
        console.debug("ready");
        return setUp();
    } else {
        return document.addEventListener('DOMContentLoaded', setUp);
    }
})();
