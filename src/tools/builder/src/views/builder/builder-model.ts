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
			this.state.activePage, widget, undefined
		);

		if (widgetElement){
			widgetElement.addEventListener("click", (event: Event) => {
				event.stopPropagation();
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
		const indexHtml: string  = result["index.html"];
		const mainPy: string  = result["main.py"];
		const pyscriptToml: string  = result["pyscript.toml"];

		console.log(indexHtml);
		console.log(mainPy);
		console.log(pyscriptToml);

		// Yo Dudes! :)
		//
		// 1) Log into psdc (prod) and generate an API Key (in your account settings).
		// 2) Paste that API key here... it will start with "psdc_".
		const apiKey = "YOUR PSDC API KEY GOES HERE";
		// 3) Put your username here :)
		const username = "YOUR PSDC USERNAME GOES HERE";
		// 4) Make up the slug for a new project (or use an existing one :).
		const projectSlug = "your-project-slug-goes-here"

		let response = await fetch(
			`/api/projects/${username}/${projectSlug}`,
			{
				method: "GET",
				headers: {
					"Authorization": `Bearer ${apiKey}`,
				}
			}
		);

		if (response.status === 404) {
			const jsonData = {
				name: projectSlug,
				description: "Testing, 1, 2, 3...",
				type: "app"
			};

			response = await fetch(
				`/api/projects/`,
				{
					method: "POST",
					headers: {
						"Authorization": `Bearer ${apiKey}`,
						'Content-Type': 'application/json',
					},
					body: JSON.stringify(jsonData)
				}
			);
		}

		if (response.status !== 200) {
			throw await response.json();
		}

		const project = await response.json();

		await Promise.all([
		    this.uploadFile(apiKey, project.id, this.createFormDataBlob('index.html', indexHtml, 'text/html')),
			this.uploadFile(apiKey, project.id, this.createFormDataBlob('pyscript.toml', pyscriptToml, 'application/toml')),
			this.uploadFile(apiKey, project.id, this.createFormDataBlob('main.py', mainPy, 'application/x-python-code')),
	  	]).then(data => {
			window.alert("Published!")
			window.open(project.latest.url, '_blank');
		});
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

	/**
	 * The path argument should be relative to the project root and contain the filename.
	 * For example: some/folder/here/file.js
	 */
	public createFormDataBlob(path: string, content = '', type = 'text/plain') {
		const blobManifest = new Blob([content], { type });
		const formData = new FormData();
		formData.append('file', blobManifest, path);
		return formData;
	}

	public async uploadFile(apiKey: string, projectId: string, formData: FormData): Promise<any> {
		const endpoint = `/api/projects/${projectId}/files?overwrite=True`;
		const response = await fetch(endpoint, {
			method: 'POST',
			body: formData,
			headers: {
				"Authorization": `Bearer ${apiKey}`,
			},
	  	});
	}
}

export const view: BuilderModel = new BuilderModel();
