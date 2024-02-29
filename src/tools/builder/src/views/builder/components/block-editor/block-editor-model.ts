import { ComponentModelBase } from "@/components/base-classes/component-model-base";
import * as Blockly from 'blockly/core';
import libraryBlocks from 'blockly/blocks';
import { pythonGenerator } from 'blockly/python';
import * as En from 'blockly/msg/en';

// Blocks
import "@/blocks/channels/definitions";
import "@/blocks/media/definitions";


/**
 *  Model for the block editor component.
 */
class BlockEditorModel extends ComponentModelBase {
    /**
	 * Specifies the localization namespace to use for getting localized text values.
	 */
	protected getLocalizationNamespace(): string {
		return "block-editor";
	}

	public init(): void {
		Blockly.setLocale(En); 

		const workspace: Blockly.WorkspaceSvg = Blockly.inject("block-editor", {
			renderer: "zelos", 
			toolbox:`<xml>
			<category name="Channels" colour="#FCC331">
			  <block type="subscribe"></block>
			</category>
			<category name="Media" colour="#ca65cc">
			  <block type="play_sound"></block>
			</category>
		  </xml>`
		});

		this.patchBlocklyFlyoutScrollbar();

		workspace.addChangeListener(() => {
			console.log(pythonGenerator.workspaceToCode(workspace));
		});
	}

	/**
	 * Patches sticky blockly flyout scrollbar when using localhost.
	 */
	private patchBlocklyFlyoutScrollbar(): void {
		if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
			const elements: NodeListOf<HTMLElement> = document.querySelectorAll(".blocklyFlyoutScrollbar");

			elements.forEach((element: HTMLElement) => {
				element.style.display = "none";
			});
		}
	}
}

export const component = new BlockEditorModel();