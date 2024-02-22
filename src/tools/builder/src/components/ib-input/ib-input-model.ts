import { ComponentModelBase } from "../base-classes/component-model-base";

/**
 * Component model for the input component.
 */
class IbInputModel extends ComponentModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "input";
	}
	
	/**
	 * Returns the value of the input.
	 */
	private getInputValue(event: Event): string {
		return (event.target as HTMLInputElement).value;
	}

	/**
	 * Updates the modelValue to that of the select box.
	 */
	public updateModelValue(event: Event, emit: Function): void {
		emit("update:modelValue", this.getInputValue(event));
		emit("input", this.getInputValue(event));
	}
}

// Export the component model
export const component: IbInputModel = new IbInputModel();