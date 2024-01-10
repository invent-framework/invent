import { ModalUtilities } from "@/utilities/modal-utilities";
import { ViewModelBase } from "../base-classes/view-model-base";
import { BuilderUtilities } from "@/utilities/builder-utilities";

/**
 * View model for the editor view.
 */
export class EditorModel extends ViewModelBase {
    /**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "editor";
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
	public onAddClicked(): void {
		ModalUtilities
	}
}