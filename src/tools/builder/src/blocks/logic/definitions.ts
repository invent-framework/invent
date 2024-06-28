import * as Blockly from 'blockly/core';

const logicColor = "#58c059";

Blockly.Blocks['logic_if'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("if");
    this.appendValueInput("if_condition")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("then");
    this.appendStatementInput("if_body")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
  }
};

Blockly.Blocks['loops_repeat'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("repeat");
    this.appendValueInput("loop_count")
        .setCheck(null);
    this.appendStatementInput("loop_body")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(logicColor);
  }
};