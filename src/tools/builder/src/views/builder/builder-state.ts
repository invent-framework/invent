import type { WidgetPropertiesModel } from "@/data/models/widget-properties-model";
import type { WidgetsModel } from "@/data/models/widgets-model";
import type { WidgetModel } from "@/data/models/widget-model";
import type { PageModel } from "@/data/models/page-model";

/**
 * View state for the builder view.
 */
export class BuilderState {
	public isAddWidgetVisible: boolean = false;

	public widgets: WidgetsModel | undefined;

	public pages: Array<PageModel> | undefined;

	public activePage: PageModel | undefined;

	public activeWidgetId: string = "";

	public activeWidgetBlueprint: WidgetModel | undefined;

	public activeWidgetProperties: WidgetPropertiesModel | undefined;

	public activeSidebarTab: string = "widgets";
}