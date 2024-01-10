import { cva } from "class-variance-authority";
import { ComponentModelBase } from "../base-classes/component-model-base";

/**
 * Component model for the button component.
 */
class IbButtonModel extends ComponentModelBase {    
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "button";
	}
    
	/**
	 * Returns list of classes for a specific button variant
	 */
	public variants: Function = cva(["inline-flex", "items-center", "border", "text-sm", "font-medium", "rounded-md", "outline-none", "focus:ring-2", "focus:ring-offset-2", "transition-all", "dark:highlight-white/5", "dark:focus:ring-offset-gray-900"], {
		variants: {
			align: {
				left: "justify-start",
				center: "justify-center",
				right: "justify-end",
			},
			size: {
				"xs": ["text-sm", "py-1.5", "px-2.5"],
				"sm": ["text-sm", "py-2", "px-4"],
				"normal": ["text-sm", "py-2.5", "px-4"]
			},
			color: {
				blue: ["bg-blue-500", "text-white", "focus:ring-blue-400", "hover:bg-blue-400", "border-transparent"],
				white: ["bg-white", "text-gray-700", "focus:ring-gray-300", "hover:bg-gray-50", "border-gray-300", "dark:bg-darkGray-900", "dark:border-darkGray-800", "dark:text-darkGray-200", "dark:hover:bg-darkGray-800"],
				green: ["bg-green-500", "text-white", "focus:ring-green-400", "hover:bg-green-400", "border-transparent"],
				navy: ["bg-navy-500", "text-white", "focus:ring-navy-400", "hover:bg-navy-400", "border-transparent"],
				red: ["bg-red-500", "text-white", "focus:ring-red-400", "hover:bg-red-400", "border-transparent"],
				transparent: ["bg-transparent", "text-gray-700", "focus:ring-transparent", "hover:bg-gray-100", "focus:bg-gray-100", "border-transparent", "dark:hover:bg-darkGray-800", "dark:focus:bg-darkGray-800", "dark:text-darkGray-200"],
				gray: ["bg-gray-100", "text-gray-700", "focus:ring-gray-200", "hover:bg-gray-200", "border-transparent", "dark:bg-darkGray-800", "dark:text-darkGray-200", "dark:hover:bg-darkGray-700"]
			},
			isFullWidth: {
				true: "w-full"
			},
			isDisabled: {
				true: ["!bg-gray-300", "!cursor-not-allowed", "focus:!ring-gray-300", "dark:!bg-darkGray-600"]
			}

		},
		defaultVariants: {
			align: "center",
			size: "normal",
			color: "blue"
		}
	});

	/**
	 * Returns an icon color based on the button color.
	 */
	public getIconColor(color?: string, isDisabled?: boolean): string {
		let iconColor: string = "";
		if (isDisabled) {
			iconColor = "white";
		}
		else {
			switch (color) {
				case "white":
					iconColor = "darkGray";
					break;
				case "transparent":
					iconColor = "darkGray";
					break;
				case "gray":
					iconColor = "darkGray";
					break;
				default:
					iconColor = "white";
					break;
			}
		}
		return iconColor;
	}
}

// Export the component model
export const component: IbButtonModel = new IbButtonModel();
