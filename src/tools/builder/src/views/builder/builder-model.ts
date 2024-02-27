import { ModalUtilities } from "@/utilities/modal-utilities";
import { ViewModelBase } from "../base-classes/view-model-base";
import { BuilderUtilities } from "@/utilities/builder-utilities";
import { BuilderState } from "./builder-state";
import { reactive } from "vue";
import type { WidgetPropertiesModel } from "@/data/models/widget-properties-model";
import type { WidgetModel } from "@/data/models/widget-model";


/**
 * View model for the builder view.
 */
export class BuilderModel extends ViewModelBase {
    /**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "builder";
	}

	/**
	 * Reactive instance of the view state.
	 */
	public state: BuilderState = reactive(new BuilderState());


	public init(): void {
		this.getPages();
		this.getAvailableComponents();
	}

	/**
	 * Widgets.
	 */

	public getAvailableComponents(): void {
		this.state.widgets = BuilderUtilities.getAvailableComponents();
	}

	public onWidgetPreviewClicked(widgetBlueprint: WidgetModel): void {
		const widgetElement: HTMLElement = BuilderUtilities.addWidgetToPage(
			this.state.activePageName, widgetBlueprint
		);

		if (widgetElement){
			widgetElement.addEventListener("click", () => {
				this.state.activeWidgetId = widgetElement.id;
				this.openPropertiesForWidget(widgetBlueprint, widgetElement.id);
			});
		}
		this.state.isAddWidgetVisible = false;
	}

	/**
	 * Called when the add button is clicked.
	 * Adds a step to the tutorial.
	 */
	public onAddPageClicked(): void {
		ModalUtilities.showModal({
			modal: "AddPage"
		});
	}

	public getPages(): any {
		this.state.pages = BuilderUtilities.getPages();
	}

	public onPageClicked(page: any): void {
		this.state.activePageName = page;
	}

	public openPropertiesForWidget(widgetBlueprint: WidgetModel, widgetRef: string): void {
		this.state.activeWidgetProperties = BuilderUtilities.getWidgetProperties(
			widgetBlueprint, widgetRef
		);
		this.state.activeWidgetBlueprint = widgetBlueprint;
	}

	public updateWidgetProperty(key: string, value: string) {
		window.console.log(this.state.activeWidgetProperties);
		window.console.log(this.state.activeWidgetBlueprint);
		BuilderUtilities.updateWidgetProperty(
			this.state.activeWidgetBlueprint, this.state.activeWidgetId, key, value
		);
	}

	public getSidebarTabColor(key: string): string { 
		return this.state.activeSidebarTab === key ? 'gray' : 'transparent';
	}
}

export const view: BuilderModel = new BuilderModel();