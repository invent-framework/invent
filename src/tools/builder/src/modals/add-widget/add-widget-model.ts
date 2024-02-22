import { FormUtilities } from "@/utilities/form-utilities";
import { ModalModelBase } from "../base-classes/modal-model-base";
// import { InventUtilities } from "@/utilities/invent-utilities";
import { ModalUtilities } from "@/utilities/modal-utilities";
// import { InventContentTypeModel } from "@/data/models/invent-content-type-model";

/**
 * Modal model for the add widget modal.
 */
class AddWidget extends ModalModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "add-widget";
	}

	public init(): void {
		FormUtilities.focusFirstInput();
	}

	/**
	 * Returns content types for a tutorial page.
	 */
	public getContentTypes(): Array<any> {
		// return InventUtilities.getContentTypes()
		return [];
	}

	public onContentTypeClicked(position: any, type: string): void {
		// InventUtilities.addContentToPage(position, type);
		ModalUtilities.closeModal();
	}
}

// Export the modal model.
export const modal: AddWidget = new AddWidget();