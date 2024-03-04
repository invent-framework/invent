import type { WidgetPropertiesModel } from "./widget-properties-model";

export interface WidgetModel {
    name: string;
    properties: WidgetPropertiesModel;
    message_blueprints: Array<string>;
    preview: string;
}