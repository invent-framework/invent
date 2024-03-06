import type { WidgetPropertiesModel } from "@/data/models/widget-properties-model";
import type { WidgetModel } from "@/data/models/widget-model";
import type { PageModel } from "@/data/models/page-model";
import type { ComponentsModel } from "@/data/models/components-model";
import type { DatastoreValueModel } from "@/data/models/datastore-value-model";
import type { DatastoreModel } from "@/data/models/datastore-model";
import type { MediaModel } from "@/data/models/media-model";

/**
 * View state for the builder view.
 */
export class BuilderState {
	public isAddWidgetVisible: boolean = false;

	public widgets: ComponentsModel | undefined;

	public pages: Array<PageModel> | undefined;

	public activePage: PageModel | undefined;

	public activeWidgetId: string = "";

	public activeWidgetBlueprint: WidgetModel | undefined;

	public activeWidgetProperties: WidgetPropertiesModel | undefined;

	public activeSidebarTab: string = "widgets";

	public activeEditorTab: string = "design";

	public activeBuilderTab: string = "app";

	public datastore: DatastoreModel = {};

	public media: MediaModel = {};

	public isPublishing: boolean = false;
}