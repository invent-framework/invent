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

	/**
	 * Initialize the view model.
	 */
	public async init(): Promise<void> {
		/**
		 * This view model has 2 sides; a JS object that looks after the UI, and a
		 * Python instance that looks after the Invent application model.
		 *
		 * Here, we wait for the Python instance to be available in the global window
		 * scope as it is created after PyScript has got an interpreter up and running.
		 */
		// @ts-ignore
		while (!window['builder']){
			await new Promise(r => setTimeout(r, 10));
		}

		/**
		 * Now we have the Python-side available, we can pass a reference to this object
		 * (i.e. the JS side) into it.
		 */
		BuilderUtilities.init(this);

		/**
		 * Start listening for messages from the host application.
		 */
		window.addEventListener("message", this.onMessage.bind(this));

		/**
		 * Let the host application know that we are ready to roll (the host should
		 * NOT send any other messages to us until this message has been received).
		 */
		window.parent.postMessage({type: "invent-ready"}, "*");
	}

	/**
	 * Load an existing Invent application.
	 */
	public async load(data: any): Promise<void> {
		// Load App.
		if(!data) {
			data = {
				"app": BuilderUtilities.getAppAsDict(),
				"media": {},
				"datastore": {},
				"blocks": {}
			}
		}
		
		BuilderUtilities.getAppFromDict(data.app);

		// TODO: Not sure we need to do this on the next tick - please check after
		// PyCon! :)
		nextTick(() => {
			this.getPages();
			this.setDefaultPage();
			this.getAvailableComponents();
		});

		// Load Media.
		// This MUST be done *before* loading the blocks as they may well reference the
		// media files.
		this.state.media = data.media;

		// Load Datastore.
		this.state.datastore = data.datastore;

		// Load Blocks.
		Blockly.serialization.workspaces.load(data.blocks, Blockly.getMainWorkspace());
	}

	/**
	 * Save the Invent application that we are currently building.
	 *
	 * We actually just serialize the application, it is up to the host to decide where
	 * it is persisted.
	 */
	public save(): any {
		const datastore: string = this.getDatastoreValues();
		const generatedCode: string = pythonGenerator.workspaceToCode(Blockly.getMainWorkspace());
		const code: string = `${this.state.functions}\n${generatedCode}`;
		const sourceCode: any = BuilderUtilities.exportAsPyScriptApp(datastore, code);

		return {
			app: JSON.stringify(BuilderUtilities.getAppAsDict(), null, 2),
			blocks: JSON.stringify(Blockly.serialization.workspaces.save(Blockly.getMainWorkspace())),
			datastore: JSON.stringify(this.state.datastore),
			sourceCode
		};
	}

	/**
	 * Called when a message is received from the host application.
	 */
	async onMessage(event: MessageEvent) {
		const { type, data } = event.data;

		console.log(`BuilderModel.onMessage: type: ${type}: `, data);

		switch (type){
			/**
			 * The host application wants us to load an Invent app from the data it
			 * passed in the event (as yet, this doesn't require a response).
			 */
			case "load-request": {
				await this.load(data);
				break;
			}

			/**
			 * The host application wants to save the Invent app that we are currently
			 * building. We just serialize the app and send it back - it is up to the
			 * host to decide where it is actually saved.
			 */
			case "save-request": {
				window.parent.postMessage({
					type: "save-response",
					data: this.save(),
				}, "*");
				break;
			}

			/**
			 * The host application has uploaded a new media file.
			 *
			 * This is in response to the 'add-media-request' we sent when the "Add"
			 * button was pressed on the Media tab.
			 */
			case "add-media-response": {
				this.state.media[data.name] = {
					name: data.name,
					type: data.type,
					path: data.path
				}
				break;
			}
		}
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

	public setComponentProperty(key: string, value: string, isLayout: boolean, isFromDatastore?: boolean,) {
		BuilderUtilities.setComponentProperty(
			this.state.activeWidgetId, key, value, isLayout, isFromDatastore
		);
	}

	public getSidebarTabColor(key: string): string {
		return this.state.activeSidebarTab === key ? 'gray' : 'transparent';
	}

	public getPageButtonColor(page: PageModel): string {
		return this.state.activePage && this.state.activeBuilderTab === 'app' && this.state.activePage.properties.id === page.properties.id ? 'gray' : 'transparent';
	}

	// Drag and Drop Prototype.
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
						BuilderUtilities.updateDatastore(
							datastoreValue.key, datastoreValue.default_value
						);
						this.state.datastore[datastoreValue.key] = datastoreValue;
						ModalUtilities.closeModal();
					}
				}
			}
		})
	}

	/**
	 * Called when the "Add" button on the Media tab is clicked.
	 */
	public onAddMediaFile(): void {
		/**
		 * Send a message to the host application to let it know that the user wants to
		 * add a media file. The host will send us an "add-media-response" message
		 * if/when a media file has been added.
		 */
		window.parent.postMessage({type: "add-media-request"}, "*");
	}

	public getImageFiles(): Array<IbSelectOption> {
		return this.filterMediaFiles("image");
	}

	public getSoundFiles(): Array<IbSelectOption> {
		return this.filterMediaFiles("audio");
	}

	private filterMediaFiles(typePrefix: string): Array<IbSelectOption> {
		const mediaFiles: Array<IbSelectOption> = Object.values(this.state.media).filter((file: MediaFileModel) => {
			return file.type.startsWith(typePrefix)
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
			...mediaFiles
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
