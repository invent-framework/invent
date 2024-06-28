import * as Blockly from 'blockly/core';

const loopsColor = "#4c97ff";

Blockly.Blocks['loops_forever'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("forever");
    this.appendStatementInput("loop_body")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(loopsColor);
  }
};

Blockly.Blocks['loops_repeat_count'] = {
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
    this.setColour(loopsColor);
  }
};