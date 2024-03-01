import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['inline_text'] = function(block: Blockly.Block) {
    const value: string = block.getFieldValue('value');
    const code = value;
    return [code, 0];  
};
  