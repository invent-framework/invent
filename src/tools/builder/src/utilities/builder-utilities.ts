import { ref, type Ref } from "vue";

 /**
 * Utility functions for the builder.
 */
export class BuilderUtilities {	
	public static app: Ref<any> = ref({
		pages: {}
	});

	public static activePage: Ref<any> = ref();

	public static createApp(): void {
		this.app.value = {
			pages: {
				"Page 1": {
					container: {
						type: "column",
						children: []
					}
				}
			}
		}
	}

	public static addPage(key: string) {
		if (this.app.value){
			this.app.value.pages[key] = {
				container: {
					type: "column",
					children: []
				}
			}
		}
	}

	public static setActivePage(page: any) {
		this.activePage.value = page;
	}

	public static widgets: Array<any> = [
		{
			type: "button"
		}
	]

	public static addWidget(widget: any, position: any) {
		position.append(widget);
	}
}