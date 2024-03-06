import { ComponentModelBase } from "../base-classes/component-model-base";

/**
 * Component model for the select component.
 */
class IbSelectModel extends ComponentModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "select";
	}
	
	/**
	 * Returns the value of the select box.
	 */
	private getSelectValue(event: Event): string {
		return (event.target as HTMLInputElement).value;
	}

	/**
	 * Updates the modelValue to that of the select box.
	 */
	public updateModelValue(event: Event, emit: Function): void {
		emit("update:modelValue", this.getSelectValue(event));
		emit("input", this.getSelectValue(event));
	}
}

// Export the component model
export const component: IbSelectModel = new IbSelectModel();