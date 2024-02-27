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
		const widgetId: string = BuilderUtilities.addWidgetToPage(
			this.state.activePage, widgetBlueprint
		);

		const widgetElement: HTMLElement | null = document.getElementById(widgetId);

		if (widgetElement){
			widgetElement.addEventListener("click", () => {
				this.state.activeWidget = widgetId;
				this.openPropertiesForWidget(widgetBlueprint, widgetId);
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
		this.state.activePage = page;
	}

	public openPropertiesForWidget(widgetBlueprint: WidgetModel, widgetRef: string): void {
		this.state.activeWidgetProperties = BuilderUtilities.getWidgetProperties(
			widgetBlueprint, widgetRef
		);
	}

	public updateWidgetProperty(value: string) {
		BuilderUtilities.updateWidgetProperty(this.state.activeWidget, value);
	}

	public getSidebarTabColor(key: string): string { 
		return this.state.activeSidebarTab === key ? 'gray' : 'transparent';
	}
}

export const view: BuilderModel = new BuilderModel();