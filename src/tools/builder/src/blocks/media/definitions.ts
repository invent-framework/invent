import * as Blockly from 'blockly/core';

Blockly.Blocks['play_sound'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("play")
          .appendField(new Blockly.FieldDropdown([["oink.mp3","oink.mp3"], ["honk.mp3","honk.mp3"]]), "sounds");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#ca65cc");
    }
};
  