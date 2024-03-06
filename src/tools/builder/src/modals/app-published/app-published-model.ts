import { ModalModelBase } from "../base-classes/modal-model-base";

/**
 * Modal model for the app published modal.
 */
export class AppPublishedModel extends ModalModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "app-published";
	}

	public onViewAppClicked(url: string) {
		window.open(url, '_blank');
	}
}