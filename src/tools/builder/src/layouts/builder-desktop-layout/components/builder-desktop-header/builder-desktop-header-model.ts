import { ComponentModelBase } from "@/components/base-classes/component-model-base";

/**
 * Component model for the builder desktop header component.
 */
export class BuilderHeaderModel extends ComponentModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "builder-desktop-header";
	}
}

// Export the component model.
export const component: BuilderHeaderModel = new BuilderHeaderModel();