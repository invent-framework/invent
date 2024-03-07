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
import { CommonUtilities } from "@/utilities/common-utilities";


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

	private apiKey = "psdc_gAAAAABl5zj-GCPoqFRv62GrpO8ud1mZhz_bbMTXSwwd1WR0ayuaiFLl15WnafvFiKMQEULC1YdSLOu4P8PEr5Cj8WPTJq2w0bgZsusOIur9UKf17tIsSlRHrDDEWLpHD1GSooHYvLNyLDFfoGDPEd50pfdoKDy8F7K3plvTjQfEC5lGnNjKt53uKlrwrEFJmLiGiV9-U4TD_uNUOAwnnIHOxMtZ0UI-MQ==";
	private username = "joshualowe1002";
	private projectSlug = CommonUtilities.getRandomId("invent", "").toLowerCase();

	/**
	 * Reactive instance of the view state.
	 */
	public state: BuilderState = reactive(new BuilderState());


	public async init(): Promise<void> {
		await this.setupProject();
		this.getPages();
		this.setDefaultPage();
		this.getAvailableComponents();
	}

	private async setupProject(): Promise<void> {
		this.state.project = await this.getProject();
		if (this.state.project === null) {
			this.state.project = await this.createProject("Invent Demo", "app");
		}
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
			widgetElement.parentElement!.addEventListener("click", (event: Event) => {
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
		this.state.activeBuilderTab = "app";
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

	public getPageButtonColor(page: PageModel): string { 
		return this.state.activePage && this.state.activeBuilderTab === 'app' && this.state.activePage.id === page.id ? 'gray' : 'transparent';
	}

	// Drag and Drop Prototype
	public onDragStart(event: DragEvent, widget: WidgetModel) {
		event.dataTransfer?.setData("widget", JSON.stringify(widget));
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

		await Promise.all([
		    this.uploadFile(this.createFormDataBlob('index.html', indexHtml, 'text/html')),
			this.uploadFile(this.createFormDataBlob('pyscript.toml', pyscriptToml, 'application/toml')),
			this.uploadFile(this.createFormDataBlob('main.py', mainPy, 'application/x-python-code')),
	  	]).then(() => {
			confetti({
				particleCount: 100,
				spread: 200
			});
	
			ModalUtilities.showModal({
				modal: "AppPublished",
				options: {
					url: this.state.project.latest.url
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

	public async getProject() {
		const response = await fetch(
			`/api/projects/${this.username}/${this.projectSlug}`,
			{
				method: "GET",
				headers: {
					"Authorization": `Bearer ${this.apiKey}`,
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

	public async createProject(description: string, type: string) {
		const response = await fetch(
			`/api/projects/`,
			{
				method: "POST",
				headers: {
					"Authorization": `Bearer ${this.apiKey}`,
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					name: this.projectSlug, description, type
				})
			}
		);

		const result = await response.json();
		if (response.status != 200) {
			throw result;
		}

		return result;
	}

	public async uploadFile(formData: FormData): Promise<any> {
		const endpoint = `/api/projects/${this.state.project.id}/files?overwrite=True`;
		const response = await fetch(endpoint, {
			method: 'POST',
			body: formData,
			headers: {
				"Authorization": `Bearer ${this.apiKey}`,
			},
	  	});

		const result = await response.json();
		if (response.status != 200) {
			throw result;
		}

		return result;
	}

	public async uploadMediaFile(file: File): Promise<string> {
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

		const path: string = `media/${mediaFolder}/${file.name}`;
		const formData: FormData = this.createFormDataFromBlob(path, file);
		this.uploadFile(formData);
		return `https://${this.username}.pyscriptapps.com/${this.projectSlug}/latest/${path}`;
	}

	public onBuilderTabClicked(tab: string) {
		this.state.activeBuilderTab = tab;

		if (tab === "blocks"){
			nextTick(() => {
				Blockly.svgResize(Blockly.getMainWorkspace() as Blockly.WorkspaceSvg);
			});
		}
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

	public onAddMediaFile(): void {
		// Create file input in order to open file chooser.
		const fileInput: HTMLInputElement = document.createElement("input");
		fileInput.type = "file";
		fileInput.accept = ".png, .jpg, .gif, .jpeg, .mp3, .wav, .mp4, .mov";

		// Runs when the user chooses a file.
		fileInput.addEventListener("change", (event: Event) => {
			const target: HTMLInputElement = event.target as HTMLInputElement;
			const reader: FileReader = new FileReader();

			reader.addEventListener("load", async (event: ProgressEvent<FileReader>) => {
				// Parse JSON file and then open the editor with its contents.
				if (event.target && target.files) {
					const file: File = target.files[0];
					const path: string = await this.uploadMediaFile(file);
					const fileName: string = file.name;
					this.state.media[fileName] = {
						name: fileName,
						type: file.type,
						file,
						path
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
		const images: Array<IbSelectOption> = Object.values(this.state.media).filter((file: MediaFileModel) => {
			return file.type.startsWith('image')
		}).map((file: MediaFileModel) => {
			return {
				label: file.name,
				value: file.path
			};
		})

		return [
			{
				label: "Select a file...",
				value: ""
			},
			...images
		]
	}

	public getSoundFiles(): Array<IbSelectOption> {
		const sounds: Array<IbSelectOption> = Object.values(this.state.media).filter((file: MediaFileModel) => {
			return file.type.startsWith('audio')
		}).map((file: MediaFileModel) => {
			return {
				label: file.name,
				value: file.path
			};
		})

		return [
			{
				label: "Select a file...",
				value: ""
			},
			...sounds
		]
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
