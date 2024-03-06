import { ModalUtilities } from "@/utilities/modal-utilities";
import { ViewModelBase } from "../base-classes/view-model-base";
import { BuilderUtilities } from "@/utilities/builder-utilities";
import { BuilderState } from "./builder-state";
import { nextTick, reactive } from "vue";
import type { WidgetModel } from "@/data/models/widget-model";
import type { PageModel } from "@/data/models/page-model";
import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';
import confetti from "canvas-confetti";
import type { DatastoreValueModel } from "@/data/models/datastore-value-model";
import type { MediaFileModel } from "@/data/models/media-file-model";
import type { IbSelectOption } from "@/components/ib-select/ib-select-types";


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
		console.log(this.state.activeWidgetProperties);
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

	public getDatastoreValues(): string {
		const datastoreCode: Array<string> = [];

		Object.values(this.state.datastore).forEach((datastoreValue: DatastoreValueModel) => {
			if (datastoreValue.temporary){
				if (datastoreValue.type === "text"){
					datastoreCode.push(`invent.datastore["${datastoreValue.key}"] = "${datastoreValue.default_value}"`);
				}
				else if (datastoreValue.type === "number"){
					datastoreCode.push(`invent.datastore["${datastoreValue.key}"] = ${datastoreValue.default_value}`);
				}
			}
			else {
				if (datastoreValue.type === "text"){
					datastoreCode.push(`invent.datastore.setdefault("${datastoreValue.key}", "${datastoreValue.default_value}")`);
				}
				else if (datastoreValue.type === "number"){
					datastoreCode.push(`invent.datastore.setdefault("${datastoreValue.key}", ${datastoreValue.default_value})`);
				}
			}
		});

		return datastoreCode.join("\n");
	}

	public async getPythonCode(): Promise<any> {
		this.state.isPublishing = true;

		const datastore: string = this.getDatastoreValues();
		const code: string = pythonGenerator.workspaceToCode(Blockly.getMainWorkspace());

		const result: any = BuilderUtilities.exportAsPyScriptApp(datastore, code);
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
		const apiKey = "YOUR API KEY GOES HERE"
		// 3) Put your username here :)
		const username = "YOUR USERNAME GOES HERE";
		// 4) Make up the slug for a new project (or use an existing one :).
		const projectSlug = "your-project-slug-goes-here"		// Yo Dudes! :)

		// Get/create the project.
		let project = await this.getProject(apiKey, username, projectSlug);
		if (project === null) {
			project = await this.createProject(apiKey, projectSlug, "Invent Demo", "app");
		}

		await Promise.all([
			this.uploadMediaFiles(apiKey, project.id),
		    this.uploadFile(apiKey, project.id, this.createFormDataBlob('index.html', indexHtml, 'text/html')),
			this.uploadFile(apiKey, project.id, this.createFormDataBlob('pyscript.toml', pyscriptToml, 'application/toml')),
			this.uploadFile(apiKey, project.id, this.createFormDataBlob('main.py', mainPy, 'application/x-python-code')),
	  	]).then(() => {
			confetti({
				particleCount: 100,
				spread: 200
			});
	
			ModalUtilities.showModal({
				modal: "AppPublished",
				options: {
					url: project.latest.url
				}
			});

			this.state.isPublishing = false;
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

	public createFormDataFromBlob(path: string, blob: Blob) {
		const formData = new FormData();
		formData.append('file', blob, path);
		return formData;
	}

	public async getProject(apiKey: string, username: string, projectSlug: string) {
		const response = await fetch(
			`/api/projects/${username}/${projectSlug}`,
			{
				method: "GET",
				headers: {
					"Authorization": `Bearer ${apiKey}`,
				}
			}
		);
		if (response.status === 404) {
			return null;
		}

		const result = await response.json();
		if (response.status != 200) {
			throw result;
		}

		return result;
	}

	public async createProject(apiKey: string, name: string, description: string, type: string) {
		const response = await fetch(
			`/api/projects/`,
			{
				method: "POST",
				headers: {
					"Authorization": `Bearer ${apiKey}`,
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					name, description, type
				})
			}
		);

		const result = await response.json();
		if (response.status != 200) {
			throw result;
		}

		return result;
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

		const result = await response.json();
		if (response.status != 200) {
			throw result;
		}

		return result;
	}

	public async uploadMediaFiles(apiKey: string, projectId: string): Promise<void> {
		const files: Array<Promise<void>> = Object.values(this.state.media).map(async (file: MediaFileModel) => {
			let mediaFolder: string = "";

			if (file.type.startsWith('image')){
				mediaFolder = "images";
			}
			else if (file.type.startsWith('audio')){
				mediaFolder = "sounds";
			}
			else if (file.type.startsWith('video')){
				mediaFolder = "videos";
			}

			const formData: FormData = this.createFormDataFromBlob(`media/${mediaFolder}/${file.name}`, file.file);
			this.uploadFile(apiKey, projectId, formData);
		});

		await Promise.all(files);
	}

	public onBuilderTabClicked(tab: string) {
		this.state.activeBuilderTab = tab;
	}

	public getBuilderTabColor(key: string): string { 
		return this.state.activeBuilderTab === key ? 'gray' : 'transparent';
	}

	public onAddDatastoreValueClicked(): void {
		ModalUtilities.showModal({
			modal: "AddDatastoreValue",
			options: {
				onAddValue: (isValid: boolean, datastoreValue: DatastoreValueModel): void => {
					if (isValid){
						this.state.datastore[datastoreValue.key] = datastoreValue;
						ModalUtilities.closeModal();
					}
				}
			}
		})
	}

	public uploadMediaFile(): void {
		// Create file input in order to open file chooser.
		const fileInput: HTMLInputElement = document.createElement("input");
		fileInput.type = "file";
		fileInput.accept = ".png, .jpg, .gif, .jpeg, .mp3, .wav, .mp4, .mov";

		// Runs when the user chooses a file.
		fileInput.addEventListener("change", (event: Event) => {
			const target: HTMLInputElement = event.target as HTMLInputElement;
			const reader: FileReader = new FileReader();

			reader.addEventListener("load", (event: ProgressEvent<FileReader>) => {
				// Parse JSON file and then open the editor with its contents.
				if (event.target && target.files) {
					const file: File = target.files[0];
					this.state.media[file.name] = {
						name: file.name,
						type: file.type,
						file
					}
				}
			});

			// Trigger reading the uploaded files.
			if (target.files) {
				reader.readAsDataURL(target.files[0]);
			}
		});

		// Click on the file input to open a file chooser.
		fileInput.click();
	}

	public getImageFiles(): Array<IbSelectOption> {
		return Object.values(this.state.media).filter((file: MediaFileModel) => {
			return file.type.startsWith('image')
		}).map((file: MediaFileModel) => {
			return {
				label: file.name,
				value: file.name
			};
		})
	}

	public getChoicePropertyOptions(options: Array<string>): Array<IbSelectOption> {
		return options.map((option: string) => {
			return {
				label: option,
				value: option
			}
		})
	}
}

export const view: BuilderModel = new BuilderModel();
