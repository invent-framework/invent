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
        this.setColour("#3EB049");
    }
};


Blockly.Blocks["listen"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField("listen")
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#9966ff");
    }
};
