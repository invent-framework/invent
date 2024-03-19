import * as Blockly from 'blockly/core';
import { view as builder } from "@/views/builder/builder-model";
import type { DatastoreValueModel } from '@/data/models/datastore-value-model';

function getDatastoreValues(): any {
    if (Object.values(builder.state.datastore).length > 0){
        return Object.values(builder.state.datastore).map((value: DatastoreValueModel) => {
            return [value.key, value.key];
        });
    }
    else {
        return [["No Datastore Values", ""]];
    }
}

Blockly.Blocks["datastore_values"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(getDatastoreValues()), "key");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#ff8c1b");
    }
};

Blockly.Blocks["get_datastore_value"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(getDatastoreValues()), "key");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#ff8c1b");
    }
};

Blockly.Blocks['set_datastore'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("set")
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
  