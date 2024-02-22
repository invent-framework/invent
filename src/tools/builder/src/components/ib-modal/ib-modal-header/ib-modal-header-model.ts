import { ComponentModelBase } from "../../base-classes/component-model-base";

/**
 * Component model for the modal header component.
 */
class IbModalHeaderModel extends ComponentModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "modal-header";
	}

	/**
	 * Returns a size for the heading component.
	 */
	public getHeadingSize(size?: string): string {
		return size ? size : "2xl";
	}
}

// Export the component model
export const component: IbModalHeaderModel = new IbModalHeaderModel();