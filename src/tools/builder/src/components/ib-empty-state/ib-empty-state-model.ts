import { cva } from "class-variance-authority";
import { ComponentModelBase } from "../base-classes/component-model-base";

/**
 * Component model for the empty state component.
 */
class IbEmptyStateModel extends ComponentModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "empty-state";
	}

	/**
	 * Returns list of classes for the empty state component.
	 */
	public variants: Function = cva(["flex", "items-center", "justify-center", "rounded-lg"], {
		variants: {
			backgroundColor: {
				lightGray: ["bg-gray-100", "dark:bg-darkGray-900"],
				gray: ["bg-gray-200", "dark:bg-darkGray-900"]
			},
			isFullHeight: {
				true: "h-full"
			},
			isFullWidth: {
				true: "w-full"
			},
		},
		defaultVariants: {
			backgroundColor: "gray"
		}
	});
}

// Export the component model
export const component: IbEmptyStateModel = new IbEmptyStateModel();