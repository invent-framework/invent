import * as Blockly from 'blockly/core';
import { view as builder } from "@/views/builder/builder-model";
import type { PageModel } from '@/data/models/page-model';

function getPages(): any {
    if (builder.state.pages && builder.state.pages.length > 0){
        return builder.state.pages.map((value: PageModel) => {
            return [value.name, value.name];
        });
    }
    else {
        return [["No Pages", ""]];
    }
}

Blockly.Blocks["pages"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(getPages()), "page");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#9966ff");
    }
};

Blockly.Blocks['show_page'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("show page");
      this.appendValueInput("page")
          .setCheck(null);
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#9966ff");
    }
};