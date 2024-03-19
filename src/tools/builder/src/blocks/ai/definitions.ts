import * as Blockly from 'blockly/core';

Blockly.Blocks["summarize"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField("summarize files")
        this.appendValueInput("files")
            .setCheck(null);        
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#3EB049");
    }
};