import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['set_datastore'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    const key: string = generator.valueToCode(block, 'key', 0);
    const value: string = generator.valueToCode(block, 'value', 0);
    const code = `invent.datastore["${key}"] = ${value}\n`;
    return code;
};

pythonGenerator.forBlock['change_datastore_value_by'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    const key: string = generator.valueToCode(block, 'key', 0);
    const value: string = generator.valueToCode(block, 'value', 0);
    const code = `invent.datastore["${key}"] = (invent.datastore["${key}"] + ${value})\n`;
    return code;
};