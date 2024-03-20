import { FormUtilities, type ValidationSchema } from "@/utilities/form-utilities";
import { ModalModelBase } from "../base-classes/modal-model-base";
import { reactive, watchEffect } from "vue";
import { AddDatastoreValueState } from "./add-datastore-value-state";
import * as yup from "yup";
import type { IbRadioGroupOption } from "@/components/ib-radio-group/ib-radio-group-types";
import { view as builder } from "@/views/builder/builder-model";


/**
 * Modal model for the add datastore value modal.
 */
export class AddDatastoreValueModel extends ModalModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "add-datastore-value";
	}

	/**
	 * Reactive instance of the modal state.
	 */
	public state: AddDatastoreValueState = reactive(new AddDatastoreValueState());


	/**
	 * Initialise the modal model.
	 */
	public init(): void {
		this.watchForFormChanges();
		FormUtilities.focusFirstInput();

		// Set Default Values
		this.state.data['type'] = "text";
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
			key: yup
				.string()
				.test("exists", "Value already exists", (value: string | undefined): boolean => {
					if (value && builder.state.datastore[value] !== undefined){
						return false;
					}
					else {
						return true;
					}
				})
				.required(FormUtilities.getValidationMessage("required", [this.getText("key")])),
			type: yup
				.string()
				.required(FormUtilities.getValidationMessage("required", [this.getText("type")])),
			default_value: yup
				.string()
				.required(FormUtilities.getValidationMessage("required", [this.getText("default-value")])),
			reset: yup
				.boolean()
		};
	}
	
	/**
	 * Validates a specified field and then updates the value of isValid to true if all fields are valid.
	 */
	public async validateField(field: string): Promise<void> {
		FormUtilities.validateField(field, this.getValidationSchema(), this.state.data, this.state.errors);
		this.state.isValid = await FormUtilities.isFormValid(this.getValidationSchema(), this.state.data);
	}

	public getTypeOptions(): Array<IbRadioGroupOption> {
		return [
			{
				key: "text",
				title: this.getText("text")
			},
			{
				key: "number",
				title: this.getText("number"),
			},
			{
				key: "boolean",
				title: "Boolean",
			},
			{
				key: "list",
				title: "List",
			},
		];
	}
}