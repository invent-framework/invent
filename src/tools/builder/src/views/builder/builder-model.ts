import { ModalUtilities } from "@/utilities/modal-utilities";
import { ViewModelBase } from "../base-classes/view-model-base";
import { BuilderUtilities } from "@/utilities/builder-utilities";
import { BuilderState } from "./builder-state";
import { reactive } from "vue";
import type { WidgetPropertiesModel } from "@/data/models/widget-properties-model";

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
		this.getAvailableWidgets();
	}

	/**
	 * Widgets.
	 */

	public onAddWidgetClicked(): void {
		this.state.isAddWidgetVisible = true;
	}

	public getAvailableWidgets(): void {
		this.state.widgets = BuilderUtilities.getAvailableWidgets();
	}

	public onWidgetClicked(): void {
		const widgetRef: string = BuilderUtilities.addWidget();
		const widgetElement: HTMLElement | null = document.getElementById(widgetRef);

		if (widgetElement){
			widgetElement.addEventListener("click", () => {
				this.state.activeWidget = widgetRef;
				this.openPropertiesForWidget(widgetRef);
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

	public openPropertiesForWidget(widgetRef: string): void {
		this.state.activeWidgetProperties = BuilderUtilities.getWidgetProperties(widgetRef);
	}

	public updateWidgetProperty(value: string) {
		BuilderUtilities.updateWidgetProperty(this.state.activeWidget, value);
	}

	public getSidebarTabColor(key: string): string { 
		return this.state.activeSidebarTab === key ? 'gray' : 'transparent';
	}
}

export const view: BuilderModel = new BuilderModel();