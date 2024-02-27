import { ComponentModelBase } from "@/components/base-classes/component-model-base";

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
					<div id="yeah-this-is-the-place" class="paper container">
					</div>
				</body>
			</html>
		`;
	}
}

export const component = new PageEditorModel();