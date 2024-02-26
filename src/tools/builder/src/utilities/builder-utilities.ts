import type { WidgetPropertiesModel } from "@/data/models/widget-properties-model";
import type { WidgetsModel } from "@/data/models/widgets-model";
import { view as builder } from '@/views/builder/builder-model';

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

	public static getAvailableWidgets(): WidgetsModel {
		return JSON.parse(this.builder().get_available_widgets());
	}

	public static addWidget(): string {
		return this.builder().add_widget_to_page("page-editor");
	}

	public static getWidgetProperties(widgetRef: string): WidgetPropertiesModel {
		return JSON.parse(this.builder().get_widget_properties(widgetRef));
	}

	public static updateWidgetProperty(widgetRef: string, value: string) {
		this.builder().update_widget_property(widgetRef, value);
	}
}