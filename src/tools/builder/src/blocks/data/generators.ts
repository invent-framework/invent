import * as Blockly from 'blockly/core';
import { PythonGenerator, pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['data_values'] = function(block: Blockly.Block) {
    const key: string = block.getFieldValue('key');
    const code = key;
    return [code, 0];  
};

pythonGenerator.forBlock['data_get_value'] = function(block: Blockly.Block) {
    const key: string = block.getFieldValue('key');
    const code = `invent.datastore["${key}"]`;
    return [code, 0];  
};

pythonGenerator.forBlock['data_set_value'] = function(block: Blockly.Block, generator: PythonGenerator) {
    const key: string = generator.valueToCode(block, 'key', 0);
    const value: string = generator.valueToCode(block, 'value', 0);
    const code = `invent.datastore["${key}"] = ${value}\n`;
    return code;
};

pythonGenerator.forBlock['data_change_value_by'] = function(block: Blockly.Block, generator: PythonGenerator) {
    const key: string = generator.valueToCode(block, 'key', 0);
    const value: string = generator.valueToCode(block, 'value', 0);
    const code = `invent.datastore["${key}"] = (invent.datastore["${key}"] + ${value})\n`;
    return code;
};