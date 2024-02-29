import { ComponentModelBase } from "@/components/base-classes/component-model-base";
import * as Blockly from 'blockly/core';
import libraryBlocks from 'blockly/blocks';
import { pythonGenerator } from 'blockly/python';
import * as En from 'blockly/msg/en';


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
			<category name="Logic" colour="%{BKY_LOGIC_HUE}">
			  <block type="controls_if"></block>
			  <block type="logic_compare"></block>
			  <block type="logic_operation"></block>
			  <block type="logic_negate"></block>
			  <block type="logic_boolean"></block>
			</category>
			<category name="Loops" colour="%{BKY_LOOPS_HUE}">
			  <block type="controls_repeat_ext">
				<value name="TIMES">
				  <block type="math_number">
					<field name="NUM">10</field>
				  </block>
				</value>
			  </block>
			  <block type="controls_whileUntil"></block>
			</category>
			<category name="Math" colour="%{BKY_MATH_HUE}">
			  <block type="math_number">
				<field name="NUM">123</field>
			  </block>
			  <block type="math_arithmetic"></block>
			  <block type="math_single"></block>
			</category>
			<category name="Text" colour="%{BKY_TEXTS_HUE}">
			  <block type="text"></block>
			  <block type="text_length"></block>
			  <block type="text_print"></block>
			</category>
			<category name="Variables" custom="VARIABLE" colour="%{BKY_VARIABLES_HUE}">
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