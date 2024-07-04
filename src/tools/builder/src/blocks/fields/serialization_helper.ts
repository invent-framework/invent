import * as Blockly from 'blockly/core';

/**
 * Returns the extra state of the given block (either as XML or a JSO, depending
 * on the block's definition).
 * @param {!Blockly.BlockSvg} block The block to get the extra state of.
 * @returns {string} A stringified version of the extra state of the given
 *     block.
 */
export function getExtraBlockState(block: Blockly.Block) {
  if (block.saveExtraState) {
    const state = block.saveExtraState();
    return state ? JSON.stringify(state) : '';
  } else if (block.mutationToDom) {
    const state = block.mutationToDom();
    return state ? Blockly.Xml.domToText(state) : '';
  }
  return '';
}