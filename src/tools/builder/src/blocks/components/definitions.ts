import * as Blockly from 'blockly/core';

const componentsColor = "#FCC331";

Blockly.Blocks['components_component_dropdown'] = {
    init: function() {
      this.appendDummyInput()
          .appendField(new Blockly.FieldDropdown([["Button1","Button1"]]), "component");
      this.setInputsInline(true);
      this.setOutput(true, null);
      this.setColour(componentsColor);
    }
};  

Blockly.Blocks['components_events_dropdown'] = {
    init: function() {
      this.appendDummyInput()
          .appendField(new Blockly.FieldDropdown([["pressed","pressed"], ["touched","touched"], ["held","held"]]), "event");
      this.setInputsInline(true);
      this.setOutput(true, null);
      this.setColour(componentsColor);
    }
};  

Blockly.Blocks['components_when'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("when")
      this.appendValueInput("component")
          .setCheck(null);
      this.appendDummyInput()
          .appendField("is")
      this.appendValueInput("event")
          .setCheck(null);
      this.appendStatementInput("function_body")
          .setCheck(null);
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(componentsColor);
    },
};