import { ComponentModelBase } from "../base-classes/component-model-base";

/**
 * Component model for the radio group component.
 */
class IbRadioGroupModel extends ComponentModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "radio-group";
	}

	/**
	 * Returns class for a radio button based on active prop.
	 */
	public getRadioButtonActiveClass(active: string, key: string): string | undefined {
		return active === key ? "bg-white ring-2 ring-violet-500" : "bg-gray-100 border-gray-300";
	}
}

// Export the component model
export const component: IbRadioGroupModel = new IbRadioGroupModel();