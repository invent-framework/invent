import * as Blockly from 'blockly/core';
import { pythonGenerator, Order } from 'blockly/python';

pythonGenerator.forBlock['logic_compare'] = function(block, generator) {
    // TODO: change Order.ATOMIC to the correct operator precedence strength
    const value_this = generator.valueToCode(block, 'this', Order.ATOMIC);
  
    const dropdown_operator = block.getFieldValue('operator');
  
    // TODO: change Order.ATOMIC to the correct operator precedence strength
    const value_that = generator.valueToCode(block, 'that', Order.ATOMIC);
  
    // TODO: Assemble python into the code variable.
    const code = '...';
    // TODO: Change Order.NONE to the correct operator precedence strength
    return [code, Order.NONE];
  }
  
pythonGenerator.forBlock['logic_boolean'] = function(block, generator) {
    // TODO: change Order.ATOMIC to the correct operator precedence strength
    const value_this = generator.valueToCode(block, 'this', Order.ATOMIC);

    const dropdown_operator = block.getFieldValue('operator');

    // TODO: change Order.ATOMIC to the correct operator precedence strength
    const value_that = generator.valueToCode(block, 'that', Order.ATOMIC);

    // TODO: Assemble python into the code variable.
    const code = '...';
    // TODO: Change Order.NONE to the correct operator precedence strength
    return [code, Order.NONE];
}

pythonGenerator.forBlock['logic_not'] = function(block, generator) {
    // TODO: change Order.ATOMIC to the correct operator precedence strength
    const value_this = generator.valueToCode(block, 'this', Order.ATOMIC);
  
    // TODO: Assemble python into the code variable.
    const code = '...';
    // TODO: Change Order.NONE to the correct operator precedence strength
    return [code, Order.NONE];
  }