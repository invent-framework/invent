import { type App } from "vue";
import { ModalName } from "./constants";

import AddPage from "./add-page/add-page.vue";

/**
 * Export & install modals for use globally
 */
export default {
	install(app: App): void {
		app.component(ModalName.AddPage, AddPage);
	}
};