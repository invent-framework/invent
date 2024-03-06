import { ComponentModelBase } from "@/components/base-classes/component-model-base";
import type { PageModel } from "@/data/models/page-model";
import type { WidgetModel } from "@/data/models/widget-model";
import { BuilderUtilities } from "@/utilities/builder-utilities";

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
				    <link rel="stylesheet" href="/css/page-editor.css">
				</head>
				<body>
				</body>
			</html>
		`;
	}

	public onPageLoad(pages: Array<PageModel>, activePage: PageModel, addWidgetToPage: Function): void {
		const pageEditor: HTMLIFrameElement = document.getElementById(`${activePage.id}-editor`) as HTMLIFrameElement;
		const pageElement: HTMLElement = BuilderUtilities.getPageElementById(activePage.id);
		pageElement.style.display = "grid";
		pageEditor.contentDocument?.body.insertBefore(pageElement, pageEditor.contentDocument?.body.firstChild);

		this.addDragAndDropEventListeners(pages, activePage, addWidgetToPage);
	}

	private addDragAndDropEventListeners(pages: Array<PageModel>, activePage: PageModel, addWidgetToPage: Function): void {
		pages.forEach((page: PageModel) => {
			const iframe: HTMLIFrameElement = document.getElementById(`${page.id}-editor`) as HTMLIFrameElement;
			
			if (iframe.contentDocument){
				const dropZoneMain: HTMLDivElement = iframe.contentDocument.createElement("div");
				const page: HTMLDivElement = iframe.contentDocument.getElementById(activePage.id) as HTMLDivElement;
				dropZoneMain.id = "drop-zone-main";
				dropZoneMain.classList.add("drop-zone");
				page.appendChild(dropZoneMain);

				dropZoneMain.addEventListener("dragover", (event: DragEvent) => {
					event.preventDefault();
					event.stopPropagation();
					dropZoneMain.classList.add("drop-zone-active");
				});

				dropZoneMain.addEventListener("dragleave", (event: DragEvent) => {
					event.preventDefault();
					event.stopPropagation();
					dropZoneMain.classList.remove("drop-zone-active");
				});

				dropZoneMain.addEventListener("drop", (event: DragEvent) => {
					event.preventDefault();
					event.stopPropagation();

					dropZoneMain.classList.remove("drop-zone-active");

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