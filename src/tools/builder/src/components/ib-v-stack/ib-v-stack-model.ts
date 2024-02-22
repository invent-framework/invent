import { cva } from "class-variance-authority";
import { ComponentModelBase } from "../base-classes/component-model-base";

/**
 * Component model for the v-stack component.
 */
class IbVStackModel extends ComponentModelBase {
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "v-stack";
	}

	/**
	 * Returns list of classes for the v-stack component.
	 */
	public variants: Function = cva(undefined, {
		variants: {
			backgroundColor: {
				white: "bg-white",
				gray: "bg-gray-100"
			},
			spacing: {
				0: "space-y-0",
				0.5: "space-y-0.5",
				1: "space-y-1",
				2: "space-y-2",
				4: "space-y-4",
				6: "space-y-6",
				8: "space-y-8",
			},
			margin: {
				"-4": "-m-4",
				"-3": "-m-3",
				"-2": "-m-2",
				"-1": "-m-1",
				"0": "m-0",
				"2": "m-2",
				"4": "m-4",
				"6": "m-6",
				"8": "m-8"
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
				true: ["h-full", "flex", "flex-col"]
			},
			isFullWidth: {
				true: "w-full"
			},
			overflow: {
				auto: ["overflow-y-auto", "overflow-x-hidden"],
				hidden: "overflow-y-hidden"
			}
		},
		defaultVariants: {
			spacing: 0
		}
	});
}

// Export the component model
export const component: IbVStackModel = new IbVStackModel();