import type { WidgetPropertiesModel } from "@/data/models/widget-properties-model";
import type { WidgetsModel } from "@/data/models/widgets-model";

/**
 * View state for the builder view.
 */
export class BuilderState {
	public isAddWidgetVisible: boolean = false;

	public widgets: WidgetsModel | undefined;

	public pages: any;

	public activePage: string = "Page1";

	public activeWidget: string = "";

	public activeWidgetProperties: WidgetPropertiesModel | undefined;

	public activeSidebarTab: string = "widgets";
}