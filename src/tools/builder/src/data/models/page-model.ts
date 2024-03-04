import type { WidgetModel } from "./widget-model";

export interface PageModel {
    id: string;
    name: string;
    element: HTMLElement;
    content: Array<WidgetModel>;
}