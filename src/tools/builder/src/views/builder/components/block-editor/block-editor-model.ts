import { ComponentModelBase } from "@/components/base-classes/component-model-base";
import * as Blockly from "blockly/core";
import * as En from "blockly/msg/en";
import * as libraryBlocks from "blockly/blocks";

// Blocks
import "@/blocks/common/definitions";
import "@/blocks/common/generators";

import "@/blocks/channels/definitions";
import "@/blocks/channels/generators";

import "@/blocks/media/definitions";
import "@/blocks/media/generators";

import "@/blocks/datastore/definitions";
import "@/blocks/datastore/generators";


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

		Blockly.inject("block-editor", {
			renderer: "zelos", 
			zoom: {
				startScale: 0.95
			},
			toolbox: this.toolbox
		});

		this.patchBlocklyFlyoutScrollbar();
	}

	private toolbox = {
		kind: "categoryToolbox",
		contents: [
			{
				kind: "category",
				name: "Channels",
				colour: "#FCC331",
				contents: [
					{
						kind: "block",
						type: "subscribe",
						inputs: {
							channels: {
								shadow: {
									type: "inline_text"
								}
							},
							subjects: {
								shadow: {
									type: "inline_text"
								}
							}
						}
					}
				]
			},
			{
				kind: "category",
				name: "Media",
				colour: "#ca65cc",
				contents: [
					{
						kind: "block",
						type: "play_sound",
						inputs: {
							file: {
								shadow: {
									type: "sound_files"
								}
							}
						}
					}
				]
			},
			{
				kind: "category",
				name: "Datastore",
				colour: "#ff8c1b",
				contents: [
					{
						kind: "block",
						type: "set_datastore",
						inputs: {
							key: {
								shadow: {
									type: "datastore_values"
								}
							},
							value: {
								shadow: {
									type: "inline_text",
									fields: {
										value: "value"
									}
								}
							}
						}
					},
					{
						kind: "block",
						type: "datastore_values"
					},
					{
						kind: "block",
						type: "change_datastore_value_by",
						inputs: {
							key: {
								shadow: {
									type: "datastore_values"
								}
							},
							value: {
								shadow: {
									type: "inline_number",
									fields: {
										value: 1
									}
								}
							}
						}
					}
				]
			},
			{
				kind: "CATEGORY",
				name: "Logic",
				colour: 210,
				contents: [
				  {
					kind: "block",
					type: "controls_if",
				  },
				  {
					kind: "block",
					type: "logic_compare",
				  },
				  {
					kind: "block",
					type: "logic_operation",
				  },
				  {
					kind: "block",
					type: "logic_negate",
				  },
				  {
					kind: "block",
					type: "logic_boolean",
				  },
				  {
					kind: "block",
					type: "logic_ternary",
				  },
				],
			  },
			  {
				kind: "CATEGORY",
				name: "Loops",
				colour: 122,
				contents: [
				  {
					kind: "block",
					type: "controls_repeat_ext",
					inputs: {
					  TIMES: {
						shadow: {
						  type: "math_number",
						  fields: {NUM: 10},
						},
					  },
					},
				  },
				  {
					kind: "block",
					type: "controls_whileUntil",
				  },
				  {
					kind: "block",
					type: "controls_for",
					inputs: {
					  FROM: {
						shadow: {
						  type: "math_number",
						  fields: {NUM: 1},
						},
					  },
					  TO: {
						shadow: {
						  type: "math_number",
						  fields: {NUM: 10},
						},
					  },
					  BY: {
						shadow: {
						  type: "math_number",
						  fields: {NUM: 1},
						},
					  },
					},
				  },
				  {
					kind: "block",
					type: "controls_forEach",
				  },
				  {
					kind: "block",
					type: "controls_flow_statements",
				  },
				],
			  },		  
		]
	};

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