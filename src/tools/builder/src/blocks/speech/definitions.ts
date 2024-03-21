import * as Blockly from 'blockly/core';

Blockly.Blocks["say"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField("say")
        this.appendValueInput("text")
            .setCheck(null);        
        this.setInputsInline(true);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour("#ca65cc");
    }
};


Blockly.Blocks["listen"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField("listen")
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#ca65cc");
    }
};


Blockly.Blocks['set_voice'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("set voice")
      this.appendDummyInput()
          .appendField("to");
      this.appendValueInput("value")
          .setCheck(null);
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#ca65cc");
    }
};
