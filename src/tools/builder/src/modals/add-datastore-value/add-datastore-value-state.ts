import type { FormData, FormErrors } from "@/utilities/form-utilities";

/**
 * View state for the add datastore value modal.
 */
export class AddDatastoreValueState {
	/**
	 * Stores data from the add page form.
	 */
	public data: FormData = {};
	 
	/**
	 * Stores a list of errors from the add page form.
	 */
	public errors: FormErrors = {};

	/**
	 * True if all fields are valid.
	 */
	public isValid: boolean = false;
}