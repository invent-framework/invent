export interface WidgetPropertyModel {
    property_type: string;
    description: string;
    required: boolean;
    default_value?: string;
    value?: string;
    min_length?: number;
    max_length?: number;
    choices: Array<string>;
    is_from_datastore: boolean;
    is_layout: boolean;
    id: string;
    name: string;
}