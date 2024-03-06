import { ComponentModelBase } from "../base-classes/component-model-base";
import type { Data } from "../types";

/**
 * Component model for the toggle component.
 */
class IbToggleModel extends ComponentModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "toggle";
	}

	/**
	 * Initialise the component model.
	 */
	public init(props: Data, emit: Function): void {
		this.setInitialValues(props, emit);
	}

	/**
	 * Sets initial form values.
	 */
	private setInitialValues(props: Data, emit: Function): void {
		if (props.modelValue === undefined) {
			emit("update:modelValue", false);
		}
	}

	/**
	 * Returns dynamic class list based on whether the toggle is toggled for the button.
	 */
	public getButtonToggledClassList(toggled?: boolean): string {
		return toggled ? "bg-violet-500" : "bg-gray-100 dark:bg-darkGray-950";
	}

	/**
	 * Returns dynamic class list based on whether the toggle is toggled for the toggle switch.
	 */
	public getToggleToggledClassList(toggled?: boolean): string {
		return toggled ? "translate-x-5" : "translate-x-0";
	}
}

// Export the component model
export const component: IbToggleModel = new IbToggleModel();