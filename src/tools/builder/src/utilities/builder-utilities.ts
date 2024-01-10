import { ref, type Ref } from "vue";

 /**
 * Utility functions for the builder.
 */
export class BuilderUtilities {	
	public static app: Ref<any | undefined> = ref(undefined);

	public static createApp(): void {
		this.app.value = {
			pages: {
				page1: {
					widgets: []
				}
			}
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

// {
// 	"pages": [
// 		{
// 			widgets: [
// 				{
// 					type: "vbox",
// 					widgets: []
// 				},
// 				{
// 					type: "button",
// 					label: "",
// 					color: ""
// 				}
// 			]
// 		}
// 	]
// }