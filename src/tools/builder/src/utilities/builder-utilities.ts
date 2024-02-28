import type { WidgetPropertiesModel } from "@/data/models/widget-properties-model";
import type { WidgetsModel } from "@/data/models/widgets-model";
import type { WidgetModel } from "@/data/models/widget-model";
import type { PageModel } from "@/data/models/page-model";

 /**
 * Utility functions for the builder.
 */
export class BuilderUtilities {	
	public static builder(): any {
		return (window as any).builder;
	} 

	public static getPages(): Array<PageModel> {
		return JSON.parse(this.builder().get_pages());
	}

	public static addPage(name: string): PageModel {
		return JSON.parse(this.builder().add_page(name));

	}

	public static getAvailableComponents(): WidgetsModel {
		return JSON.parse(this.builder().get_available_components());
	}

	public static addWidgetToPage(activePage: PageModel | undefined , widgetBlueprint: WidgetModel): HTMLElement {
		return this.builder().add_widget_to_page(activePage, widgetBlueprint);
	}

	public static getWidgetProperties(widgetBlueprint: WidgetModel, widgetRef: string): WidgetPropertiesModel {
		return JSON.parse(this.builder().get_widget_properties(
			widgetBlueprint, widgetRef
		));
	}

	public static updateWidgetProperty(widgetBlueprint: WidgetModel | undefined, widgetRef: string, key: string, value: string) {
		this.builder().update_widget_property(widgetBlueprint, widgetRef, key, value);
	}
}