import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['inline_text'] = function(block: Blockly.Block) {
    const value: string = block.getFieldValue('value');
    const code = value;
    return [code, 0];  
};

pythonGenerator.forBlock['inline_number'] = function(block: Blockly.Block) {
    const value: string = block.getFieldValue('value');
    const code = value;
    return [code, 0];  
};
  

pythonGenerator.forBlock['inline_string'] = function(block: Blockly.Block) {
    const value: string = block.getFieldValue('value');
    const code = value;
    return [code, 0];  
};
  