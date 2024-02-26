import type { WidgetPropertiesModel } from "./widget-properties-model";

export interface WidgetModel {
    properties: WidgetPropertiesModel;
    message_blueprints: Array<string>;
    preview: string;
}