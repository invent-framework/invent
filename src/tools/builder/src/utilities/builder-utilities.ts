import { ref, type Ref } from "vue";

 /**
 * Utility functions for the builder.
 */
export class BuilderUtilities {	
	public static app: Ref<any> = ref({
		pages: {}
	});

	public static activePage: Ref<string | undefined> = ref();

	public static createApp(): void {
		this.app.value = {
			pages: {}
		}
	}

	public static addPage(key: string) {
		if (this.app.value){
			this.app.value.pages[key] = {
				widgets: []
			}
		}
	}

	public static setActivePage(key: string) {
		this.activePage.value = key;
	}

	public static getPage(key: string): object {
		return this.app.value.pages[key];
	}
}