import { ComponentModelBase } from "@/components/base-classes/component-model-base";
import type { PageModel } from "@/data/models/page-model";
import type { WidgetModel } from "@/data/models/widget-model";

/**
 *  Model for the page editor component.
 */
class PageEditorModel extends ComponentModelBase {
    /**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "page-editor";
	}

	public getSrcDoc() : string {
		return `
			<html>
				<head>
				    <link rel="stylesheet" href="https://unpkg.com/papercss@1.9.2/dist/paper.min.css">
				</head>
				<body>
					<div id="container" class="paper container">
					</div>
				</body>
			</html>
		`;
	}

	public addDragAndDropEventListeners(pages: Array<PageModel>, activePage: PageModel, addWidgetToPage: Function): void {
		pages.forEach((page: PageModel) => {
			const iframe: HTMLIFrameElement = document.getElementById(page.id) as HTMLIFrameElement;
			
			if (iframe.contentDocument){
				iframe.contentDocument.addEventListener("dragover", (event: DragEvent) => {
					event.preventDefault();
				});

				iframe.contentDocument.addEventListener("drop", (event: DragEvent) => {
					event.preventDefault();

					if (page.id === activePage.id){
						const widget: WidgetModel = JSON.parse(event.dataTransfer?.getData("widget") as string);
						addWidgetToPage(widget);
					}
				});
			}
		});
	}
}

export const component = new PageEditorModel();