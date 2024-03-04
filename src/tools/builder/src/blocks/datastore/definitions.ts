import * as Blockly from 'blockly/core';

Blockly.Blocks['set_datastore'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("set");
      this.appendValueInput("key")
          .setCheck(null);
      this.appendDummyInput()
          .appendField("to");
      this.appendValueInput("value")
          .setCheck(null);
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#ff8c1b");
    }
};
  
Blockly.Blocks['change_datastore_value_by'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("change");
      this.appendValueInput("key")
          .setCheck(null);
      this.appendDummyInput()
          .appendField("by");
      this.appendValueInput("value")
          .setCheck(null);
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#ff8c1b");
    }
};
  