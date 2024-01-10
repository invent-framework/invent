import { LocalizationUtilities } from "@/utilities/localization-utilities";
import { ModalUtilities } from "@/utilities/modal-utilities";

/**
 * Base class exposing common functionality to all modal models.
 */
export abstract class ModalModelBase {
	/**
	 * Return the string that is used for the localization namespace when getting localized text for the modal.
	 * This is an abstract property that needs to be defined in the modal model that extends this base class.
	 */
	protected abstract getLocalizationNamespace(): string;

	/**
	 * Uses the specified key (and value of the 'localizationNamespace' property) to lookup localized text for displaying in the modal.
	 */
	public getText(key: string, placeholderValues?: Array<string>): string {
		return LocalizationUtilities.getLocalizedText(this.getLocalizationNamespace(), key, placeholderValues);
	}

	/**
	 * Called when the user clicks a button to close the modal.
	 */
	public onCloseClicked(): void {
		ModalUtilities.closeModal();
	}
}