import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['channels_subscribe'] = function(block, generator) {
    const value_function_name = generator.valueToCode(block, 'function_name', python.Order.ATOMIC);
    const value_message = generator.valueToCode(block, 'message', python.Order.ATOMIC);
    const value_channel = generator.valueToCode(block, 'channel', python.Order.ATOMIC);
    // TODO: Assemble python into code variable.
    const code = '...\n';
    return code;
};

pythonGenerator.forBlock['channels_unsubscribe'] = function(block, generator) {
    const value_function_name = generator.valueToCode(block, 'function_name', python.Order.ATOMIC);
    const value_message = generator.valueToCode(block, 'message', python.Order.ATOMIC);
    const value_channel = generator.valueToCode(block, 'channel', python.Order.ATOMIC);
    // TODO: Assemble python into code variable.
    const code = '...\n';
    return code;
};

pythonGenerator.forBlock['channels_publish'] = function(block, generator) {
    const value_message = generator.valueToCode(block, 'message', python.Order.ATOMIC);
    const value_channel = generator.valueToCode(block, 'channel', python.Order.ATOMIC);
    // TODO: Assemble python into code variable.
    const code = '...\n';
    return code;
};

pythonGenerator.forBlock['channels_create_message'] = function(block, generator) {
    const value_subject = generator.valueToCode(block, 'subject', python.Order.ATOMIC);
    const value_data = generator.valueToCode(block, 'data', python.Order.ATOMIC);
    // TODO: Assemble python into code variable.
    const code = '...\n';
    return code;
};