import { BuilderUtilities } from '@/utilities/builder-utilities';
import * as Blockly from 'blockly/core';

const channelsColor = "#ffac1a";

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

Blockly.Blocks["channels_channels"] = {
  init: function(): void {
      this.appendDummyInput()
          .appendField(new Blockly.FieldDropdown(getChannels()), "channel");
      this.setInputsInline(true);
      this.setOutput(true, null);
      this.setColour("#FCC331");
  }
};

Blockly.Blocks["channels_subjects"] = {
  init: function(): void {
      this.appendDummyInput()
          .appendField(new Blockly.FieldDropdown(getSubjects()), "subject");
      this.setInputsInline(true);
      this.setOutput(true, null);
      this.setColour("#FCC331");
  }
};

Blockly.Blocks['channels_subscribe'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("subscribe");
    this.appendValueInput("function_name")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("to");
    this.appendValueInput("message")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("on");
    this.appendValueInput("channel")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(channelsColor);
  }
};

Blockly.Blocks['channels_unsubscribe'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("unsubscribe");
    this.appendValueInput("function_name")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("from");
    this.appendValueInput("message")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("on");
    this.appendValueInput("channel")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(channelsColor);
  }
};


Blockly.Blocks['channels_publish'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("publish");
    this.appendValueInput("message")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("to");
    this.appendValueInput("channel")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(channelsColor);
  }
};

Blockly.Blocks['channels_create_message'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("create message with subject");
    this.appendValueInput("subject")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("and data");
    this.appendValueInput("data")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(channelsColor);
  }
};