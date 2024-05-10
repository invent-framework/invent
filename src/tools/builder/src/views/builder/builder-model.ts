import { ModalUtilities } from "@/utilities/modal-utilities";
import { ViewModelBase } from "../base-classes/view-model-base";
import { BuilderUtilities } from "@/utilities/builder-utilities";
import { BuilderState } from "./builder-state";
import { nextTick, reactive } from "vue";
import type { WidgetModel } from "@/data/models/widget-model";
import type { PageModel } from "@/data/models/page-model";
import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';
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

	public async init(): Promise<void> {
		/**
		 * Wait for the "builder" object to be available in the global scope.
		 */
		// @ts-ignore
		while (!window['builder']){
			await new Promise(r => setTimeout(r, 10));
		}

		this.getPages();
		this.setDefaultPage();
		this.getAvailableComponents();
		/*
			* BuilderUtilities is really just a bridge between this class (the JS-side of
			* the view model) and the "Builder" class in "builder.py" (the Python-side of
			* the view model).
			*/
		BuilderUtilities.init(this);

		this.listenForIframeMessages();

		window.parent.postMessage({
			type: "invent-ready"
		}, location.origin);
	}

	// Pages ///////////////////////////////////////////////////////////////////////////

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

	public listenForIframeMessages(): void {
		window.addEventListener("message", async (event: MessageEvent) => {
			// Only allow same origin messages.
  		if (event.origin !== location.origin) return;

			const { type, data } = event.data;

			console.log(`Invent - received message type ${type}:`, data);

			switch (type){
				case "save-request": {
					event.source?.postMessage({
						type: "save-response",
						data: this.save(),
					});

					break;
				}

				case "load-request": {
					await this.load(data);
					break;
				}

				case "media-upload-complete": {
					this.state.media[data.name] = {
						name: data.name,
						type: data.type,
						path: data.path
					}
					break;
				}
			}
		});
	}

	/**
	 * Called when the add page button is clicked.
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

	/**
	 * Called when a page button is clicked.
	 */
	public onPageClicked(page: PageModel): void {
		this.state.activeBuilderTab = "app";
		this.setActivePage(page);
	}

	// Components //////////////////////////////////////////////////////////////////////

	public getAvailableComponents(): void {
		this.state.widgets = BuilderUtilities.getAvailableComponents();
	}

	public addComponentToPage(widgetBlueprint: WidgetModel) {
		let parentId: any;

		if (!this.state.activeWidgetId) {
			parentId = this.state.activePage?.properties?.id;
		} else {
			if (["Row", "Page", "Column", "Grid"].includes(this.state.activeWidgetBlueprint?.name as string)) {
				parentId = this.state.activeWidgetId;
			} else {
				// If a widget (hint, not a container) is selected, should we add to the
				// page or to the selected widget's parent?
				parentId = this.state.activePage?.properties?.id;
			}
		}

		BuilderUtilities.createAndAppendComponent(parentId, widgetBlueprint.name);
	}

	public openPropertiesForComponent(componentBlueprintJSON: string, componentId: string): void {
		this.state.activeWidgetId = componentId;
		this.state.activeWidgetBlueprint = JSON.parse(componentBlueprintJSON);
		this.state.activeWidgetProperties = BuilderUtilities.getComponentProperties(componentId);
	}

	public setComponentProperty(key: string, value: string, isFromDatastore?: boolean) {
		BuilderUtilities.setComponentProperty(
			this.state.activeWidgetId, key, value, isFromDatastore
		);
	}

	public getSidebarTabColor(key: string): string {
		return this.state.activeSidebarTab === key ? 'gray' : 'transparent';
	}

	public getPageButtonColor(page: PageModel): string {
		return this.state.activePage && this.state.activeBuilderTab === 'app' && this.state.activePage.properties.id === page.properties.id ? 'gray' : 'transparent';
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
				else if (datastoreValue.type === "boolean"){
					datastoreCode.push(`invent.datastore["${datastoreValue.key}"] = ${datastoreValue.default_value}`);
				}
				else if (datastoreValue.type === "list"){
					datastoreCode.push(`invent.datastore["${datastoreValue.key}"] = []`);
				}
			}
			else {
				if (datastoreValue.type === "text"){
					datastoreCode.push(`invent.datastore.setdefault("${datastoreValue.key}", "${datastoreValue.default_value}")`);
				}
				else if (datastoreValue.type === "number"){
					datastoreCode.push(`invent.datastore.setdefault("${datastoreValue.key}", ${datastoreValue.default_value})`);
				}
				else if (datastoreValue.type === "boolean"){
					datastoreCode.push(`invent.datastore.setdefault("${datastoreValue.key}", ${datastoreValue.default_value})`);
				}
				else if (datastoreValue.type === "list"){
					datastoreCode.push(`invent.datastore.setdefault("${datastoreValue.key}", [])`);
				}
			}
		});

		return datastoreCode.join("\n");
	}

	public async load(data: any): Promise<void> {
		// Load App
		BuilderUtilities.getAppFromDict(data.app);
		this.state.pages = [];
		nextTick(() => {
			// this.init();
			this.getPages();
			this.setDefaultPage();
			this.getAvailableComponents();
		});

		// Load media (this MUST be done before loading the blocks so that it can
		// reference the media files in blocks such as playing sounds etc.).
		this.state.media = data.media;

		// Load Blocks
		Blockly.serialization.workspaces.load(data.blocks, Blockly.getMainWorkspace());

		// Load Datastore
		this.state.datastore = data.datastore;

	}

	public save(): any {
		const datastore: string = this.getDatastoreValues();
		const generatedCode: string = pythonGenerator.workspaceToCode(Blockly.getMainWorkspace());
		const code: string = `${this.state.functions}\n${generatedCode}`;
		const psdc: any = BuilderUtilities.exportAsPyScriptApp(datastore, code);

		return {
			app: JSON.stringify(BuilderUtilities.getAppAsDict()),
			blocks: JSON.stringify(Blockly.serialization.workspaces.save(Blockly.getMainWorkspace())),
			datastore: JSON.stringify(this.state.datastore),
			psdc
		};
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

	public onBuilderTabClicked(tab: string) {
		this.state.activeBuilderTab = tab;

		if (tab === "blocks"){
			nextTick(() => {
				Blockly.svgResize(Blockly.getMainWorkspace() as Blockly.WorkspaceSvg);
				const xml = Blockly.Xml.workspaceToDom(Blockly.getMainWorkspace());
				Blockly.getMainWorkspace().clear();
				Blockly.Xml.domToWorkspace(xml, Blockly.getMainWorkspace());
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
		window.parent.postMessage({
			type: "add-media-request",
		});
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

	public getDatastoreOptions(): Array<IbSelectOption> {
		const values: Array<IbSelectOption> = Object.values(this.state.datastore).map((value: DatastoreValueModel) => {
			return {
				label: value.key,
				value: value.key
			};
		})

		if (values.length === 0){
			return [
				{
					label: "No Datastore Values",
					value: ""
				}
			]
		}
		else {
			return [
				{
					label: "Select a value...",
					value: ""
				},
				...values
			]
		}
	}

	public deleteComponent() {
		BuilderUtilities.deleteComponent(this.state.activeWidgetId);
		this.state.activeWidgetId = "";
		this.state.activeWidgetBlueprint = undefined;
		this.state.activeWidgetProperties = undefined;
	}
}

export const view: BuilderModel = new BuilderModel();
