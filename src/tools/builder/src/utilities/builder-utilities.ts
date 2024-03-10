import type { WidgetPropertiesModel } from "@/data/models/widget-properties-model";
import type { WidgetsModel } from "@/data/models/widgets-model";
import type { WidgetModel } from "@/data/models/widget-model";
import type { PageModel } from "@/data/models/page-model";
import { view as builder } from "@/views/builder/builder-model";
import type { ComponentsModel } from "@/data/models/components-model";

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

	public static getPageElementById(pageId: string): HTMLElement {
		return this.builder().get_page_element_by_id(pageId);
	}

	public static addPage(name: string): PageModel {
		return JSON.parse(this.builder().add_page(name));
	}

	public static getAvailableComponents(): ComponentsModel {
		return JSON.parse(this.builder().get_available_components());
	}

	public static addWidgetToPage(activePage: PageModel | undefined , widgetBlueprint: WidgetModel, parentId: string | undefined): HTMLElement {
		const widgetElement: HTMLElement = this.builder().add_widget_to_page(activePage, widgetBlueprint, parentId);

		if (activePage && (widgetBlueprint.name === "Row" || widgetBlueprint.name === "Column")) {
			widgetElement.addEventListener("dragover", (event: DragEvent) => {
				event.preventDefault();
				event.stopPropagation();
				widgetElement.classList.add("drop-zone-active");
			});
	
			widgetElement.addEventListener("dragleave", (event: DragEvent) => {
				event.preventDefault();
				event.stopPropagation();
				widgetElement.classList.remove("drop-zone-active");
			});
	
			widgetElement.addEventListener("drop", (event: DragEvent) => {
				event.preventDefault();
				event.stopPropagation();
				widgetElement.classList.remove("drop-zone-active");
				
				const widgetToAdd: WidgetModel = JSON.parse(event.dataTransfer?.getData("widget") as string);
				const widgetInRowColumn: HTMLElement = this.addWidgetToPage(activePage, widgetToAdd, widgetElement.id);
				
				widgetInRowColumn.parentElement!.addEventListener("click", (event: Event) => {
					event.stopPropagation();
					builder.state.activeWidgetId = widgetInRowColumn.id;
					builder.openPropertiesForWidget(widgetToAdd, widgetInRowColumn.id);
				})
			});
	
		}

		return widgetElement;
	}

	public static getWidgetProperties(widgetBlueprint: WidgetModel, widgetRef: string): WidgetPropertiesModel {
		return JSON.parse(this.builder().get_widget_properties(
			widgetBlueprint, widgetRef
		));
	}

	public static getChannels(): Array<string> {
		return JSON.parse(this.builder().get_channels());
	}

	public static getSubjects(): Array<string> {
		return JSON.parse(this.builder().get_subjects());
	}

	public static updateWidgetProperty(widgetBlueprint: WidgetModel | undefined, widgetRef: string, key: string, value: string, isFromDatastore?: boolean) {
		this.builder().update_widget_property(widgetBlueprint, widgetRef, key, value, isFromDatastore);
	}

	public static exportAppAsPythonCode(code: string): string {
		return this.builder().export_app_as_python_code(code);
	}

	public static exportAsPyScriptApp(datastore: string, code: string): string {
		return JSON.parse(
			this.builder().export_as_pyscript_app(datastore, code)
		);
	}
}