import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['media_sound_files'] = function(block: Blockly.Block) {
    const file: string = block.getFieldValue('file');
    const code = file;
    return [code, 0];  
};

pythonGenerator.forBlock['media_play_sound'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    const file: string = generator.valueToCode(block, 'file', 0);
    const code = `invent.play_sound(invent.media.sounds.${file})\n`;
    return code;
};
  
  