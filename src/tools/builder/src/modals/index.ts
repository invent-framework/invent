import { type App } from "vue";
import { ModalName } from "./constants";

import AddWidget from "./add-widget/add-widget-model.vue";

/**
 * Export & install modals for use globally
 */
export default {
	install(app: App): void {
		app.component(ModalName.AddWidget, AddWidget);
	}
};