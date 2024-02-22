import { type Modal } from "@/modals/constants";
import { ref, type Ref } from "vue";

/**
 * Data model for a modal.
 */
export interface ModalModel {
	modal: Modal;
	options?: ModalOptions;
}

/**
 * Data model for modal options.
 */
export interface ModalOptions {
	[key: string]: any;
}

/**
 * Utility functions for screen size.
 */
export class ModalUtilities {
	/**
	 * Returns the currently set modal for the app.
	 */
	public static currentModal: Ref<ModalModel | undefined> = ref();

	/**
	 * Shows a modal by setting the current modal in the application state.
	 */
	public static showModal(modal: ModalModel): void {
		this.currentModal.value = modal;
	}
	
	/**
	 * Closes a modal by setting the current modal to undefined.
	 */
	public static closeModal(): void {
		this.currentModal.value = undefined;
	}
}