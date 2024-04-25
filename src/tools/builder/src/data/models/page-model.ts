import type { WidgetModel } from "./widget-model";
import type { WidgetPropertiesModel } from "./widget-properties-model";

export interface PageModel {
    name: string;
    element: HTMLElement;
    properties: WidgetPropertiesModel;
    content: Array<WidgetModel>;
}