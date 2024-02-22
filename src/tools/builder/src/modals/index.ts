import { type App } from "vue";
import { ModalName } from "./constants";

import AddWidget from "./add-widget/add-widget.vue";
import AddPage from "./add-page/add-page.vue";

/**
 * Export & install modals for use globally
 */
export default {
	install(app: App): void {
		app.component(ModalName.AddWidget, AddWidget);
		app.component(ModalName.AddPage, AddPage);
	}
};