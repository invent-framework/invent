import { ModalUtilities } from "@/utilities/modal-utilities";
import { ViewModelBase } from "../base-classes/view-model-base";
import { BuilderUtilities } from "@/utilities/builder-utilities";
import { BuilderState } from "./builder-state";
import { nextTick, reactive } from "vue";
import type { WidgetModel } from "@/data/models/widget-model";
import type { PageModel } from "@/data/models/page-model";
import * as Blockly from 'blockly/core';


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
		this.setDefaultPage();
		this.getAvailableComponents();
	}

	/**
	 * Widgets.
	 */

	public getAvailableComponents(): void {
		this.state.widgets = BuilderUtilities.getAvailableComponents();
	}

	public addWidgetToPage(widget: WidgetModel) {
		const widgetElement: HTMLElement = BuilderUtilities.addWidgetToPage(
			this.state.activePage, widget
		);

		if (widgetElement){
			widgetElement.addEventListener("click", () => {
				this.state.activeWidgetId = widgetElement.id;
				this.openPropertiesForWidget(widget, widgetElement.id);
			});
		}
	}

	/**
	 * Called when the add button is clicked.
	 * Adds a step to the tutorial.
	 */
	public onAddPageClicked(): void {
		ModalUtilities.showModal({
			modal: "AddPage",
			options: {
				onAddPage: (pageName: string) => {
					const page: PageModel = BuilderUtilities.addPage(pageName);
					this.getPages();
					this.setActivePage(page);
					ModalUtilities.closeModal();
				}
			}
		});
	}

	public getPages(): void {
		this.state.pages = BuilderUtilities.getPages();
	}

	public setActivePage(page: PageModel): void {
		this.state.activePage = page;
	}

	public setDefaultPage(): void {
		if (this.state.pages){
			this.setActivePage(this.state.pages[0])
		}
	}

	public onPageClicked(page: PageModel): void {
		this.setActivePage(page);
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

	public getEditorTabColor(key: string): string { 
		return this.state.activeEditorTab === key ? 'gray' : 'transparent';
	}

	public getPageButtonColor(page: PageModel): string { 
		return this.state.activePage && this.state.activePage.id === page.id ? 'gray' : 'transparent';
	}

	// Drag and Drop Prototype
	public onDragStart(event: DragEvent, widget: WidgetModel) {
		event.dataTransfer?.setData("widget", JSON.stringify(widget));
	}

	public onEditorTabClicked(tab: string) {
		this.state.activeEditorTab = tab;

		if (tab === "blocks"){
			nextTick(() => {
				Blockly.svgResize(Blockly.getMainWorkspace() as Blockly.WorkspaceSvg);
			});
		}
	}
}

export const view: BuilderModel = new BuilderModel();