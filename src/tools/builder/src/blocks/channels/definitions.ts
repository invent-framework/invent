import * as Blockly from 'blockly/core';

Blockly.Blocks['subscribe'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Subscribe");
      this.appendStatementInput("on_subject")
          .setCheck(null);
      this.appendDummyInput()
          .appendField("To Channel(s)");
      this.appendValueInput("channels")
          .setCheck(null);
      this.appendEndRowInput();
      this.appendDummyInput()
          .appendField("When Subject(s)");
      this.appendValueInput("subjects")
          .setCheck(null);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#FCC331");
    }
};
  