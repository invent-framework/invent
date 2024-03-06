import * as Blockly from 'blockly/core';
import { view as builder } from "@/views/builder/builder-model";
import type { MediaFileModel } from '@/data/models/media-file-model';

function getSoundFiles(): any {
  const audioFiles: Array<MediaFileModel> = Object.values(builder.state.media).filter((file: MediaFileModel) => {
    return file.type.startsWith("audio")
  });

  if (audioFiles.length > 0){
      return audioFiles.map((file: MediaFileModel) => {
          return [file.name, file.name];
      });
  }
  else {
      return [["No Sound Files", ""]];
  }
}

Blockly.Blocks["sound_files"] = {
  init: function(): void {
      this.appendDummyInput()
          .appendField(new Blockly.FieldDropdown(getSoundFiles()), "file");
      this.setInputsInline(true);
      this.setOutput(true, null);
      this.setColour("#ca65cc");
  }
};

Blockly.Blocks['play_sound'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("play");
      this.appendValueInput("file")
          .setCheck(null);
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#ca65cc");
    }
};
  