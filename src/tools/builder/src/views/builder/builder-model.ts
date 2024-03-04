import { ModalUtilities } from "@/utilities/modal-utilities";
import { ViewModelBase } from "../base-classes/view-model-base";
import { BuilderUtilities } from "@/utilities/builder-utilities";
import { BuilderState } from "./builder-state";
import { nextTick, reactive } from "vue";
import type { WidgetModel } from "@/data/models/widget-model";
import type { PageModel } from "@/data/models/page-model";
import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';
import JSZip from "jszip";


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
		console.log(BuilderUtilities.getPages())
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

	public async getPythonCode(): Promise<any> {
		const code: string = pythonGenerator.workspaceToCode(Blockly.getMainWorkspace());
		const result: any = BuilderUtilities.exportAsPyScriptApp(code);

		console.log(result["index.html"]);
		console.log(result["main.py"]);
		console.log(result["pyscript.toml"]);

		this.downloadFiles(
			result["index.html"],
			result["main.py"],
			result["pyscript.toml"]
		);

		// const response = await fetch(
		// "https://pyscript-dev.com/api/projects/healthz",
		// {method: "GET"}
		// );
		// console.log(`Status: ${response.status}`);
		// console.log(await response.json());

		// const apiKey = "psdc_gAAAAABleI0zc55xr4UMlABZsWQX4i_tJ7XH7SvV8vXbzeC0F62HLvADCR-hXM5JZ30pkHrbRWOg-oJX7BXE-dMIaJq3DbDX38AjXPZmXKkBfeBtlZ0_S1MscTI_8cX4LLJREQb8Fd6-Wyi-4WesU97p2d_xgYIatUWNMptfHVgnOARJY8n6C-lD4U-5jPqhn9h1bHvLVZFC-az5RH4clE5mfwazJ09HjQ==";

		// const response = await fetch(
		// 	"https://pyscript-dev.com/api/projects/jdjdjdjjdjd/versions",
		// 	{
		// 		method: "GET",
		// 		headers: {
		// 			"Authorization": `Bearer ${apiKey}`,
		// 		}
		// 	}
		// );
		// console.log(`Status: ${response.status}`);
		// console.log(await response.json());
	}

	public downloadFiles(index: string, main: string, config: string) {
		const zip = new JSZip();

		// Add files to the zip
		zip.file("index.html", index);
		zip.file("main.py", main);
		zip.file("pyscript.toml", config);
		// Add more files as needed

		// Generate the zip file asynchronously
		zip.generateAsync({type:"blob"}).then(function(content: any) {
			// Create a dummy anchor element
			const link = document.createElement("a");
			link.download = "invent.zip"; // The name of the zip file
			link.href = URL.createObjectURL(content);
			link.click(); // Simulate a click on the link

			// Clean up
			setTimeout(function() {
				URL.revokeObjectURL(link.href);
			}, 100);
		});
	}

}

export const view: BuilderModel = new BuilderModel();
