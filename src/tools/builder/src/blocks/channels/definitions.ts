import { BuilderUtilities } from '@/utilities/builder-utilities';
import * as Blockly from 'blockly/core';

function getChannels(): any {
    const channels: Array<string> = BuilderUtilities.getChannels();
    if (channels.length > 0){
        return channels.map((channel: string) => {
            return [channel, channel];
        });
    }
    else {
        return [["No Channels", ""]];
    }
}

function getSubjects(): any {
    const subjects: Array<string> = BuilderUtilities.getSubjects();
    if (subjects.length > 0){
        return subjects.map((subject: string) => {
            return [subject, subject];
        });
    }
    else {
        return [["No Subjects", ""]];
    }
}

Blockly.Blocks["channels"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(getChannels()), "channel");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#FCC331");
    }
};

Blockly.Blocks["subjects"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(getSubjects()), "subject");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#FCC331");
    }
};

Blockly.Blocks['subscribe'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Subscribe");
      this.appendStatementInput("on_subject")
          .setCheck(null);
      this.appendDummyInput()
          .appendField("To Channel");
      this.appendValueInput("channels")
          .setCheck(null);
      this.appendEndRowInput();
      this.appendDummyInput()
          .appendField("When Subject");
      this.appendValueInput("subjects")
          .setCheck(null);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#FCC331");
    }
};
  