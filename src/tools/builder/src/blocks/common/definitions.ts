import * as Blockly from 'blockly/core';
import { FieldString } from '../fields/field-string';

Blockly.Blocks["inline_text"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField(new Blockly.FieldTextInput(""), "value");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#FFFFFF");
    }
};

Blockly.Blocks["inline_string"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField(new FieldString(""), "value");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#FFFFFF");
    }
};

Blockly.Blocks["inline_number"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField(new Blockly.FieldNumber(1), "value");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#FFFFFF");
    }
};