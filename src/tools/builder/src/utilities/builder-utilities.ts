import type { WidgetPropertiesModel } from "@/data/models/widget-properties-model";
import type { WidgetsModel } from "@/data/models/widgets-model";
import { view as builder } from '@/views/builder/builder-model';
import type { WidgetModel } from "@/data/models/widget-model";

 /**
 * Utility functions for the builder.
 */
export class BuilderUtilities {	
	public static builder(): any {
		return (window as any).builder;
	} 

	public static getPages() {
		return JSON.parse(this.builder().get_pages());
	}

	public static addPage(name: string) {
		this.builder().add_page(name);
		builder.getPages();
	}

	public static getAvailableComponents(): WidgetsModel {
		return JSON.parse(this.builder().get_available_components());
	}

	public static addWidgetToPage(activePageName: string , widgetBlueprint: WidgetModel): HTMLElement {
		return this.builder().add_widget_to_page(activePageName, widgetBlueprint);
	}

	public static getWidgetProperties(widgetBlueprint: WidgetModel, widgetRef: string): WidgetPropertiesModel {
		return JSON.parse(this.builder().get_widget_properties(
			widgetBlueprint, widgetRef
		));
	}

	public static updateWidgetProperty(widgetRef: string, value: string) {
		this.builder().update_widget_property(widgetRef, value);
	}
}