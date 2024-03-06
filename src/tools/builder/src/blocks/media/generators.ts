import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['sound_files'] = function(block: Blockly.Block) {
    const file: string = block.getFieldValue('file');
    const code = file;
    return [code, 0];  
};

pythonGenerator.forBlock['play_sound'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    const file: string = generator.valueToCode(block, 'file', 0);
    const code = `invent.play_sound("${file}")\n`;
    return code;
};
  
  