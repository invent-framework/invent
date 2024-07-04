import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['media_sound_files'] = function(block: Blockly.Block) {
    const file: string = block.getFieldValue('file');
    const code = file;
    return [code, 0];  
};
  
  