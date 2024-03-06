import { type App } from "vue";
import { ModalName } from "./constants";

import AddPage from "./add-page/add-page.vue";
import AddDatastoreValue from "./add-datastore-value/add-datastore-value.vue";
import AppPublished from "./app-published/app-published.vue";

/**
 * Export & install modals for use globally
 */
export default {
	install(app: App): void {
		app.component(ModalName.AddPage, AddPage);
		app.component(ModalName.AddDatastoreValue, AddDatastoreValue);
		app.component(ModalName.AppPublished, AppPublished);
	}
};