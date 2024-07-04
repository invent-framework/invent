import * as Blockly from 'blockly/core';
import { ObservableProcedureModel, ProcedureCreate } from '@blockly/block-shareable-procedures';

const functionsColor = "#ff6680";

Blockly.Blocks['functions_define'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("define")
        .appendField(new Blockly.FieldTextInput(""), "NAME");
    this.appendStatementInput("function_body")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(functionsColor);

    this.model_ = new ObservableProcedureModel(
      this.workspace,
      Blockly.Procedures.findLegalName(this.getFieldValue('NAME'), this),
    );

    Blockly.Events.disable();
    this.workspace.getProcedureMap().add(this.getProcedureModel());
    Blockly.Events.enable();
  },

  model_: null,
  hasStatements_: true,

  getProcedureModel() {
    return this.model_;
  },

  isProcedureDef() {
    return true;
  },

  destroy: function () {
    if (!this.isInsertionMarker()) {
      this.workspace
        .getProcedureMap()
        .delete(this.getProcedureModel().getId());
    }
  },

  saveExtraState: function (doFullSerialization: boolean) {
    const state = Object.create(null);
    state['procedureId'] = this.getProcedureModel().getId();

    if (doFullSerialization) {
      state['fullSerialization'] = true;
    }
    if (!this.hasStatements_) {
      state['hasStatements'] = false;
    }
    return state;
  },

  loadExtraState: function (state: any) {
    const map = this.workspace.getProcedureMap();

    const procedureId = state['procedureId'];
    if (map.has(procedureId) && !state['fullSerialization']) {
      if (map.has(this.model_.getId())) {
        map.delete(this.model_.getId());
      }
      this.model_ = map.get(procedureId);
    }

    this.doProcedureUpdate();
  },

  onchange: function (e: any) {
    if (e.type === Blockly.Events.BLOCK_CREATE && e.blockId === this.id) {
      Blockly.Events.fire(
        new ProcedureCreate(this.workspace, this.getProcedureModel()),
      );
    }
    if (
      e.type === Blockly.Events.BLOCK_CHANGE &&
      e.blockId === this.id &&
      e.element === 'disabled'
    ) {
      this.getProcedureModel().setEnabled(this.isEnabled());
    }
  },

  doProcedureUpdate: function () {
    this.setFieldValue(this.getProcedureModel().getName(), 'NAME');
    this.setEnabled(this.getProcedureModel().getEnabled());
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
  },

  model_: null,

  getProcedureModel() {
    return this.model_;
  },

  findProcedureModel_(name: string) {
    const workspace = this.getTargetWorkspace_();
    const model = workspace
      .getProcedureMap()
      .getProcedures()
      .find((proc: any) => proc.getName() === name);
    if (!model) return null;

    return model;
  },

  getTargetWorkspace_() {
    return this.workspace.isFlyout
      ? this.workspace.targetWorkspace
      : this.workspace;
  },

  isProcedureDef() {
    return false;
  },

  saveExtraState: function () {
    const state = Object.create(null);
    const model = this.getProcedureModel();
    if (!model) {
      // We reached here because we've deserialized a caller into a workspace
      // where its model did not already exist (no procedures array in the json,
      // and deserialized before any definition block), and are reserializing
      // it before the event delay has elapsed and change listeners have run.
      // (If they had run, we would have found or created a model).
      // Just reserialize any deserialized state. Nothing should have happened
      // in-between to change it.
      state['name'] = this.getFieldValue('NAME');
      return state;
    }
    state['name'] = model.getName();
    return state;
  },

  /**
   * Applies the given state to this block.
   *
   * @param state The state to apply to this block, ie the params and
   *     procedure name.
   */
  loadExtraState: function (state: any) {
    this.deserialize_(state['name']);
  },

  /**
   * Applies the given name and params from the serialized state to the block.
   *
   * @param name The name to apply to the block.
   * @param params The parameters to apply to the block.
   */
  deserialize_: function (name: string) {
    this.setFieldValue(name, 'NAME');
    if (!this.model_) this.model_ = this.findProcedureModel_(name);
    if (this.getProcedureModel()) {
      this.doProcedureUpdate();
    }
  },

   /**
   * Updates the shape of this block to reflect the state of the data model.
   */
   doProcedureUpdate: function () {
    if (!this.getProcedureModel()) return;
    this.updateName_();
  },

  /**
   * Updates the name field of this block to match the state of the data model.
   */
  updateName_: function () {
    const name = this.getProcedureModel().getName();
    this.setFieldValue(name, 'NAME');
  },
};
