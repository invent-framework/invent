import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['play_sound'] = function(block: Blockly.Block) {
    const sounds: string = block.getFieldValue('sounds');
    const code = `invent.play_sound("${sounds}")\n`;
    return code;
};
  
  