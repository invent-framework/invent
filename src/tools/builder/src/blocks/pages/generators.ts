import * as Blockly from 'blockly/core';
import { PythonGenerator, pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['pages_pages'] = function(block: Blockly.Block) {
    const page: string = block.getFieldValue('page');
    const code = page;
    return [code, 0];  
};

pythonGenerator.forBlock['pages_show_page'] = function(block: Blockly.Block, generator: PythonGenerator) {
    const page: string = generator.valueToCode(block, 'page', 0);
    const code = `invent.show_page("${page}")\n`;
    return code;
};