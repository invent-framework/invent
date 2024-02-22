import { ModalUtilities } from "@/utilities/modal-utilities";
import { ViewModelBase } from "../base-classes/view-model-base";
import { BuilderUtilities } from "@/utilities/builder-utilities";

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

	public init(): void {
		BuilderUtilities.createApp();
	}

	public onAddWidgetClicked(): void {
		ModalUtilities.showModal({
			modal: "AddWidget"
		});
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

	public getPages(): object {
		return BuilderUtilities.app.value.pages;
	}

	public onPageClicked(page: any): void {
		BuilderUtilities.setActivePage(page);
	}
}