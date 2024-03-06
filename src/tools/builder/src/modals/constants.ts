/**
 * List of modal names.
 */
export enum ModalName {
	AddPage = "AddPage",
	AddDatastoreValue = "AddDatastoreValue",
	AppPublished = "AppPublished",
}

/**
 * List of available modals.
 */
export type Modal = 
 | "AddPage"
 | "AddDatastoreValue"
 | "AppPublished"