import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['loops_forever'] = function(block, generator) {
    const statements_loop_body = generator.statementToCode(block, 'loop_body');
    const code = '...\n';
    return code;
};

pythonGenerator.forBlock['loops_repeat'] = function(block, generator) {
    const value_loop_count = generator.valueToCode(block, 'loop_count', python.Order.ATOMIC);
    const statements_loop_body = generator.statementToCode(block, 'loop_body');
    // TODO: Assemble python into code variable.
    const code = '...\n';
    return code;
};
  
  