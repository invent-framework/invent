import { ViewModelBase } from "../base-classes/view-model-base";

/**
 * View model for the editor view.
 */
export class EditorModel extends ViewModelBase {
    /**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "editor";
	}
}