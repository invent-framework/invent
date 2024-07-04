import * as Blockly from 'blockly/core';
import { pythonGenerator, Order } from 'blockly/python';

pythonGenerator.forBlock['channels_channels'] = function(block: Blockly.Block) {
    const channel: string = block.getFieldValue('channel');
    const code = channel;
    return [code, 0];  
};

pythonGenerator.forBlock['channels_subjects'] = function(block: Blockly.Block) {
    const subject: string = block.getFieldValue('subject');
    const code = subject;
    return [code, 0];  
};

pythonGenerator.forBlock['channels_subscribe'] = function(block, generator) {
    const value_function_name = generator.valueToCode(block, 'function_name', Order.ATOMIC);
    const value_message = generator.valueToCode(block, 'message', Order.ATOMIC);
    const value_channel = generator.valueToCode(block, 'channel', Order.ATOMIC);
    // TODO: Assemble python into code variable.
    const code = '...\n';
    return code;
};

pythonGenerator.forBlock['channels_unsubscribe'] = function(block, generator) {
    const value_function_name = generator.valueToCode(block, 'function_name', Order.ATOMIC);
    const value_message = generator.valueToCode(block, 'message', Order.ATOMIC);
    const value_channel = generator.valueToCode(block, 'channel', Order.ATOMIC);
    // TODO: Assemble python into code variable.
    const code = '...\n';
    return code;
};

pythonGenerator.forBlock['channels_publish'] = function(block, generator) {
    const value_message = generator.valueToCode(block, 'message', Order.ATOMIC);
    const value_channel = generator.valueToCode(block, 'channel', Order.ATOMIC);
    // TODO: Assemble python into code variable.
    const code = '...\n';
    return code;
};

pythonGenerator.forBlock['channels_create_message'] = function(block, generator) {
    const value_subject = generator.valueToCode(block, 'subject', Order.ATOMIC);
    const value_data = generator.valueToCode(block, 'data', Order.ATOMIC);
    // TODO: Assemble python into code variable.
    const code = '...\n';
    return code;
};