import { FormUtilities, type ValidationSchema } from "@/utilities/form-utilities";
import { ModalModelBase } from "../base-classes/modal-model-base";
import { reactive, watchEffect } from "vue";
import { AddPageState } from "./add-page-state";
import * as yup from "yup";


/**
 * Modal model for the add page modal.
 */
export class AddPageModel extends ModalModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "add-page";
	}

	/**
	 * Reactive instance of the modal state.
	 */
	public state: AddPageState = reactive(new AddPageState());


	/**
	 * Initialise the modal model.
	 */
	public init(): void {
		this.watchForFormChanges();
		FormUtilities.focusFirstInput();
	}
	
	/**
	 * Watches for changes on the form and checks if it's valid.
	 */
	private watchForFormChanges(): void {
		watchEffect(async () => {
			this.state.isValid = await FormUtilities.isFormValid(this.getValidationSchema(), this.state.data);
		});
	}
	
	/**
	 * Returns validation schema for the add page form.
	 */
	public getValidationSchema(): ValidationSchema {
		return {
			name: yup
				.string()
				.required(FormUtilities.getValidationMessage("required", [this.getText("name")]))
		};
	}
	
	/**
	 * Validates a specified field and then updates the value of isValid to true if all fields are valid.
	 */
	public async validateField(field: string): Promise<void> {
		FormUtilities.validateField(field, this.getValidationSchema(), this.state.data, this.state.errors);
		this.state.isValid = await FormUtilities.isFormValid(this.getValidationSchema(), this.state.data);
	}
}