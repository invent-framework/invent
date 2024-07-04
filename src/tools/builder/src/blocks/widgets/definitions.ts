import type { WidgetModel } from '@/data/models/widget-model';
import { BuilderUtilities } from '@/utilities/builder-utilities';
import * as Blockly from 'blockly/core';

const widgetsColor = "#FCC331";

function getWidgets(): any {
    const widgets: Array<any> = BuilderUtilities.getWidgetsInAppWithMessages();
    if (widgets.length > 0){
        return widgets.map((widget: WidgetModel) => {
            return [widget.properties["id"], widget.properties["id"]];
        });
    }
    else {
        return [["No Widgets", ""]];
    }
  }

Blockly.Blocks['widgets_widgets'] = {
    init: function() {
      this.appendDummyInput()
          .appendField(new Blockly.FieldDropdown(getWidgets()), "widget");
      this.setInputsInline(true);
      this.setOutput(true, null);
      this.setColour(widgetsColor);
    }
};  

Blockly.Blocks['widgets_events'] = {
    init: function() {
      this.appendDummyInput()
          .appendField(new Blockly.FieldDropdown([["pressed","press"], ["touched","touch"]]), "event");
      this.setInputsInline(true);
      this.setOutput(true, null);
      this.setColour(widgetsColor);
    }
};  

Blockly.Blocks['widgets_when'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("when")
      this.appendValueInput("widget")
          .setCheck(null);
      this.appendDummyInput()
          .appendField("is")
      this.appendValueInput("event")
          .setCheck(null);
      this.appendStatementInput("function_body")
          .setCheck(null);
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(widgetsColor);
    },
};