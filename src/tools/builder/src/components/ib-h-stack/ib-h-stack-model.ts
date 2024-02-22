import { cva } from "class-variance-authority";
import { ComponentModelBase } from "../base-classes/component-model-base";

/**
 * Component model for the h-stack component.
 */
class IbHStackModel extends ComponentModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "h-stack";
	}

	/**
	 * Returns list of classes for the h-stack component.
	 */
	public variants: Function = cva(["flex"], {
		variants: {
			backgroundColor: {
				white: "bg-white",
				gray: "bg-gray-100"
			},
			spacing: {
				0: "space-x-0",
				1: "space-x-1",
				2: "space-x-2",
				4: "space-x-4",
				6: "space-x-6",
				8: "space-x-8",
				24: "space-x-24",
			},
			alignX: {
				left: "justify-start",
				center: "justify-center",
				right: "justify-end",
			},
			alignY: {
				top: "items-start",
				center: "items-center",
				bottom: "items-end",
			},
			justifyContent: {
				between: "justify-between",
			},
			paddingT: {
				0: "pt-0",
				2: "pt-2",
				4: "pt-4",
				6: "pt-6",
				8: "pt-8",
				10: "pt-10"
			},
			paddingB: {
				0: "pb-0",
				2: "pb-2",
				4: "pb-4",
				6: "pb-6",
				8: "pb-8",
				10: "pb-10"
			},
			paddingL: {
				0: "pl-0",
				2: "pl-2",
				4: "pl-4",
				6: "pl-6",
				8: "pl-8",
				10: "pl-10"
			},
			paddingR: {
				0: "pr-0",
				2: "pr-2",
				4: "pr-4",
				6: "pr-6",
				8: "pr-8",
				10: "pr-10"
			},
			isFullHeight: {
				true: "h-full"
			},
			isFullPageHeight: {
				true: "h-page"
			},
			isFullWidth: {
				true: "w-full"
			}
		},
		defaultVariants: {
			spacing: 0
		}
	});
}

// Export the component model
export const component: IbHStackModel = new IbHStackModel();