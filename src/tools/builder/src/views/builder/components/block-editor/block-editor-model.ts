import { ComponentModelBase } from "@/components/base-classes/component-model-base";
import * as Blockly from "blockly/core";
import * as En from "blockly/msg/en";
import "blockly/blocks";
import '@blockly/block-plus-minus';

// Blocks
import "@/blocks/common/definitions";
import "@/blocks/components/definitions";
import "@/blocks/data/definitions";
import "@/blocks/media/definitions";
import "@/blocks/channels/definitions";
import "@/blocks/loops/definitions";
import "@/blocks/logic/definitions";


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
				name: "Components",
				colour: "#FCC331",
				contents: [
					{
						kind: "label",
						text: "Components"
					},
					{
						kind: "block",
						type: "components_when",
						inputs: {
							component: {
								shadow: {
									type: "components_component_dropdown"
								}
							},
							event: {
								shadow: {
									type: "components_events_dropdown"
								}
							},
						}
					}
				]
			},
			{
				kind: "category",
				name: "Data",
				colour: "#ff8c1b",
				contents: [
					{
						kind: "label",
						text: "Data"
					},
					{
						kind: "block",
						type: "data_set_value",
						inputs: {
							key: {
								shadow: {
									type: "data_values"
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
						type: "data_change_value_by",
						inputs: {
							key: {
								shadow: {
									type: "data_values"
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
					},
					{
						kind: "block",
						type: "data_get_value"
					}
				]
			},
			{
				kind: "category",
				name: "Media",
				colour: "#ca65cc",
				contents: [
					{
						kind: "label",
						text: "Media"
					},
					{
						kind: "block",
						type: "media_play_sound",
						inputs: {
							file: {
								shadow: {
									type: "media_sound_files"
								}
							}
						}
					},
				]
			},
			{
				kind: "category",
				name: "Channels",
				colour: "#ffac1a",
				contents: [
					{
						kind: "label",
						text: "Channels"
					},
					{
						kind: "block",
						type: "channels_subscribe",
						inputs: {
							message: {
								shadow: {
									type: "channels_subjects"
								}
							},
							channel: {
								shadow: {
									type: "channels_channels"
								}
							}
						}
					},
					{
						kind: "block",
						type: "channels_unsubscribe",
						inputs: {
							message: {
								shadow: {
									type: "channels_subjects"
								}
							},
							channel: {
								shadow: {
									type: "channels_channels"
								}
							}
						}
					},
					{
						kind: "block",
						type: "channels_publish",
						inputs: {
							message: {
								shadow: {
									type: "inline_text",
									fields: {
										value: "message"
									}
								}
							},
							channel: {
								shadow: {
									type: "channels_channels"
								}
							}
						}
					},
					{
						kind: "block",
						type: "channels_create_message",
						inputs: {
							subject: {
								shadow: {
									type: "inline_text",
									fields: {
										value: ""
									}
								}
							}
						}
					}
				]
			},
			{
				kind: "category",
				name: "Loops",
				colour: "#4c97ff",
				contents: [
					{
						kind: "label",
						text: "Loops"
					},
					{
						kind: "block",
						type: "loops_forever",
					},
					{
						kind: "block",
						type: "loops_repeat_count",
						inputs: {
							loop_count: {
								shadow: {
									type: "inline_number",
									fields: {
										value: 10
									}
								}
							}
						}
					},
				]
			},
			{
				kind: "category",
				name: "Logic",
				colour: "#58c059",
				contents: [
					{
						kind: "label",
						text: "Logic"
					},
					{
						kind: "block",
						type: "controls_if",
					}
				]
			},
			{
				kind: "category",
				name: "Functions",
				colour: "#ff6680",
				custom: "FUNCTIONS"
			}
		]
	};

	/**
	 * Patches sticky blockly flyout scrollbar when using localhost.
	 */
	private patchBlocklyFlyoutScrollbar(): void {
		const elements: NodeListOf<HTMLElement> = document.querySelectorAll(".blocklyFlyoutScrollbar");

		elements.forEach((element: HTMLElement) => {
			element.style.display = "none";
		});
	}
}

export const component = new BlockEditorModel();