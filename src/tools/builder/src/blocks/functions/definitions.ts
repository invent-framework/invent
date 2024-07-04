import * as Blockly from 'blockly/core';
import { ObservableProcedureModel } from '@blockly/block-shareable-procedures';

const functionsColor = "#ff6680";

Blockly.Blocks['functions_define'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("define")
        .appendField(new Blockly.FieldTextInput(""), "function_name");
    this.appendStatementInput("function_body")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(functionsColor);

    this.model = new ObservableProcedureModel(this.workspace, Blockly.Procedures.findLegalName(this.getFieldValue('function_name'), this));

    Blockly.Events.disable();
    this.workspace.getProcedureMap().add(this.getProcedureModel());
    Blockly.Events.enable();
  },

  model: null,

  saveExtraState() {
    
  },

  loadExtraState(state: any) {
    //
  },


  getProcedureModel() {
    return this.model;
  },

  isProcedureDef() {
    return true;
  }
};

Blockly.Blocks['functions_call'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("call")
        .appendField(new Blockly.FieldLabelSerializable(""), "NAME");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(functionsColor);
  }
};