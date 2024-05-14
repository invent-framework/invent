import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';


pythonGenerator.forBlock['say'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    const text: string = generator.valueToCode(block, 'text', 0);
    const code = `invent.say(${text})`;
    return code;
};


pythonGenerator.forBlock['listen'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    const code = `await invent.listen()`;
    return [code, 0];  
};


pythonGenerator.forBlock['set_voice'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    const value: string = generator.valueToCode(block, 'value', 0);
    const code = `invent.set_voice(${value})\n`;
    return code;
};
