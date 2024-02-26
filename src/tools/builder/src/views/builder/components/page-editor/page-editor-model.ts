import { ComponentModelBase } from "@/components/base-classes/component-model-base";

/**
 *  Model for the page editor component.
 */
export class PageEditorModel extends ComponentModelBase {
    /**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "page-editor";
	}
}