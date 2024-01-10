import { ref, type Ref } from "vue";

 /**
 * Utility functions for the builder.
 */
export class BuilderUtilities {	
	public static app: Ref<any> = ref({
		pages: {}
	});

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
}