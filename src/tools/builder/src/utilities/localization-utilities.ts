import { type LocalizationNamespaceModel } from "@/data/models/localization-namespace-model";
import { type LocalizationTableModel } from "@/data/models/localization-table-model";
import { type Ref, ref } from "vue";

/**
 * Utility functions for localization.
 */
export class LocalizationUtilities {
	/**
	 * Returns the currently selected language.
	 */
	public static language: Ref<string> = ref("en");

	/**
	 * Lookup localized text and get a localized value.
	 */
	public static getText(key: string, placeholderValues?: Array<string>): string {
		return this.getLocalizedText("localization", key, placeholderValues);
	}
		
	/**
	 * Returns a list of supported languages.
	 */ 
	public static supportedLanguages: Array<string> = ["en"];

	/**
	 * Stores language resource strings for localization.
	 */
	private static textLookupTable: Ref<LocalizationTableModel> = ref({});

	/**
	 * Take namespace for view/component and key to return a translated value from the lookup table.
	 */
	public static getLocalizedText(namespace: string, key: string, placeholderValues?: Array<string>): string {
		const target: string = `${namespace}.${key}`;
		let result: string = "";

		if (this.textLookupTable.value[namespace]) {
			result = this.textLookupTable.value[namespace][key];
			// Iterate through placeholder values and replace them in the result string.
			if (placeholderValues) {
				placeholderValues.forEach((placeholder: string, index: number) => {
					result = result.replace(`{${index+1}}`, placeholder);
				});
			}
		
			if (!this.textLookupTable.value[namespace][key]) {
				return `!! ${target} !!`;
			}
		}

		return result;
	}

	/**
	 * Merge a new selected languages' strings into the lookup table.
	 */
	private static mergeNewLanguage(data: LocalizationTableModel): void {
		for (const key of Object.keys(data)) {
			this.textLookupTable.value[key] = data[key];
		}
	}

	/**
	 * Load a new language from its JSON file.
	 */
	private static async loadLanguage(code: string): Promise<LocalizationTableModel> {
		let result: LocalizationTableModel = {};

		const response: Response = await fetch(`${import.meta.env.BASE_URL}/languages/${code}.json`);

		if (response.ok) {
			result = await response.json() as LocalizationTableModel;
		}

		return result;
	}

	/**
	 * Load and set a new language.
	 */
	public static async loadPreferredLanguageAsync(): Promise<boolean> {
		const defaultLanguage: string = "en";

		if (localStorage.getItem("language")) {
			this.language.value = localStorage.getItem("language") as string;
		}

		let preferredLanguage: string = defaultLanguage;

		if (this.supportedLanguages.includes(this.language.value)) {
			preferredLanguage = this.language.value;
		}

		this.textLookupTable.value = await this.loadLanguage(defaultLanguage);

		if (preferredLanguage !== defaultLanguage) {
			const alternativeLanguageData: LocalizationTableModel = await this.loadLanguage(preferredLanguage);
			this.mergeNewLanguage(alternativeLanguageData);
		}

		return true;
	}

	/**
	 * Returns a category from the localization table.
	 */
	public static getCategory(namespace: string): LocalizationNamespaceModel {
		return this.textLookupTable.value[namespace];
	}
}