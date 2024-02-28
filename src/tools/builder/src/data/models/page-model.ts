import type { WidgetModel } from "./widget-model";

export interface PageModel {
    id: string;
    name: string;
    content: Array<WidgetModel>;
}