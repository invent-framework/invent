import type { WidgetPropertiesModel } from "@/data/models/widget-properties-model";
import type { WidgetModel } from "@/data/models/widget-model";
import type { PageModel } from "@/data/models/page-model";
import {BuilderModel, view as builder} from "@/views/builder/builder-model";
import type { ComponentsModel } from "@/data/models/components-model";
import type { WidgetPropertyModel } from "@/data/models/widget-property-model";

 /**
 * Utility functions for the builder.
 */
export class BuilderUtilities {	
	public static init(builderModel: BuilderModel): any {
		(window as any).builder.set_js_builder_model(builderModel)
	}

	public static builder(): any {
		return (window as any).builder;
	} 

	// Pages ///////////////////////////////////////////////////////////////////////////

	public static getPages(): Array<PageModel> {
		return JSON.parse(this.builder().get_pages());
	}

	public static showPage(pageId: WidgetPropertyModel): HTMLElement {
		return this.builder().show_page(pageId);
	}

	public static addPage(name: string): PageModel {
		return JSON.parse(this.builder().add_page(name));
	}

	// Components //////////////////////////////////////////////////////////////////////

	public static createAndAppendComponent(parentId: string, componentTypeName: string): void {
		this.builder().create_and_append_component(parentId, componentTypeName);
	}

	public static deleteComponent(componentId: string) {
		this.builder().delete_component(componentId);
	}

	public static getAvailableComponents(): ComponentsModel {
		return JSON.parse(this.builder().get_available_components());
	}

	public static getComponentProperties(componentId: string): WidgetPropertiesModel {
		return JSON.parse(this.builder().get_component_properties(componentId));
	}
	
	public static setComponentProperty(componentId: string, key: string, value: string, isFromDatastore?: boolean) {
		this.builder().set_component_property(componentId, key, value, isFromDatastore);
	}
	
	public static getWidgetsInAppWithMessages(): Array<WidgetModel> {
		return JSON.parse(this.builder().get_widgets_in_app_with_messages());
	}

	// Channels ////////////////////////////////////////////////////////////////////////

	public static getChannels(): Array<string> {
		return JSON.parse(this.builder().get_channels());
	}

	public static getSubjects(): Array<string> {
		const subjects = JSON.parse(this.builder().get_subjects());
		const datastoreKeys = Object.keys(builder.state.datastore);
		return [...subjects, ...datastoreKeys];
	}

	// Import/export ///////////////////////////////////////////////////////////////////

	public static exportAppAsPythonCode(code: string): string {
		return this.builder().export_app_as_python_code(code);
	}

	public static exportAsPyScriptApp(datastore: string, code: string): string {
		return JSON.parse(this.builder().export_as_pyscript_app(datastore, code));
	}

	public static getAppAsDict(): object {
		return JSON.parse(this.builder().get_app_as_dict());
	}

	public static getAppFromDict(app_dict: object): any {
		this.builder().get_app_from_dict(JSON.stringify(app_dict));
	}
}
