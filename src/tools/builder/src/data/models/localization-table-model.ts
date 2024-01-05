import { type LocalizationNamespaceModel } from "./localization-namespace-model";

/**
 * Data model for a localization table.
 */
export interface LocalizationTableModel {
	[key: string]: LocalizationNamespaceModel;
}