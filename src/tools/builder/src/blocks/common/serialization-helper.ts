import * as Blockly from 'blockly/core';

// eslint-disable-next-line consistent-return
export function getExtraBlockState(block: Blockly.BlockSvg): string | undefined {
	if (block.saveExtraState) {
		const state: any = block.saveExtraState();
		return state ? JSON.stringify(state) : "";
	}
	else if (block.mutationToDom) {
		const state: any = block.mutationToDom();
		return state ? Blockly.Xml.domToText(state) : "";
	}
}