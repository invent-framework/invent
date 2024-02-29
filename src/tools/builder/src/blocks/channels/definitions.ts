import * as Blockly from 'blockly/core';

Blockly.Blocks['subscribe'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Subscribe");
      this.appendStatementInput("NAME")
          .setCheck(null);
      this.appendDummyInput()
          .appendField("To Channel(s)")
          .appendField(new Blockly.FieldTextInput(""), "channels");
      this.appendDummyInput()
          .appendField("When Subject(s)")
          .appendField(new Blockly.FieldTextInput(""), "subjects");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#FCC331");
    }
};