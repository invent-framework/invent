import { type App } from "vue";
import { WidgetName } from "./constants";

import InventButton from "./invent-button.vue";

/**
 * Export & install invent widgets for use globally
 */
export default {
	install(app: App): void {
		app.component(WidgetName.InventButton, InventButton);
	}
};