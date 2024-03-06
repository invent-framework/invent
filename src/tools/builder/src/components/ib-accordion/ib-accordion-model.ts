import { ref, type Ref } from "vue";
import { ComponentModelBase } from "../base-classes/component-model-base";

/**
 * Component model for the accordion component.
 */
export class IbAccordionModel extends ComponentModelBase {    
	/**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "accordion";
	}
    
	public isOpen: Ref<boolean> = ref(true);

	public getIcon(): Array<string> {
		return this.isOpen.value ? ["fas", "chevron-up"] : ["fas", "chevron-down"];
	}
}