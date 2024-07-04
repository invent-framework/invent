import * as Blockly from 'blockly/core';
import { createMinusField } from '../fields/field_minus';
import { createPlusField } from '../fields/field_plus';

const logicColor = "#58c059";

Blockly.Blocks['logic_if'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("if");
    this.appendValueInput("IF0")
        .setCheck('Boolean');
    this.appendDummyInput()
        .appendField("then");
    this.appendStatementInput("DO0")
        .setCheck(null);
    this.appendDummyInput("ADDBUTTON")
        .appendField(createPlusField(), 'PLUS')
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(logicColor);
  },

  elseIfCount_: 0,

  hasElse_: false,

  saveExtraState: function () {
    if (!this.elseIfCount_ && !this.hasElse_) {
      return null;
    }
    const state = Object.create(null);
    if (this.elseIfCount_) {
      state['elseIfCount'] = this.elseIfCount_;
    }
    if (this.hasElse_) {
      state['hasElse'] = true;
    }
    return state;
  },

  loadExtraState: function (state: any) {
    const targetCount = state['elseIfCount'] || 0;
    this.hasElse_ = state['hasElse'] || false;
    if (this.hasElse_ && !this.getInput('ELSE')) {
      this.appendDummyInput("ELSETITLE")
          .appendField("else")
          .appendField(createMinusField({ else: true }), 'MINUS' + this.elseIfCount_);
      this.appendStatementInput('ELSE');
      this.createAddButton()
    }
    this.updateShape_(targetCount);
  },

  updateShape_: function (targetCount: number) {
    while (this.elseIfCount_ < targetCount) {
      this.addElseIf_();
    }
    while (this.elseIfCount_ > targetCount) {
      this.removeElseIf_();
    }
  },

  plus: function () {
    if (!this.hasElse_){
      this.appendDummyInput("ELSETITLE")
        .appendField("else")
        .appendField(createMinusField({ else: true }), 'MINUS' + this.elseIfCount_);
      this.appendStatementInput('ELSE');
      this.createAddButton()
      this.hasElse_ = true;
    }
    else {
      this.addElseIf_();
    }
  },

  minus: function (args: any) {
    if (args.else){
      this.removeInput("ELSETITLE");
      this.removeInput("ELSE");
      this.hasElse_ = false;
    }
    else {
      if (this.elseIfCount_ == 0) {
        return;
      }
      this.removeElseIf_(args.index);
    }
  },

  createAddButton: function () {
    if (this.getInput("ADDBUTTON")){
      this.removeInput("ADDBUTTON")
    }
    this.appendDummyInput("ADDBUTTON")
      .appendField(createPlusField(), 'PLUS')
  },

  addElseIf_: function () {
    // Because else-if inputs are 1-indexed we increment first, decrement last.
    this.elseIfCount_++;

    this.appendValueInput('IF' + this.elseIfCount_)
      .setCheck('Boolean')
      .appendField("else if")
    
    this.appendDummyInput("IFBUTTONS" + this.elseIfCount_)
      .appendField(createMinusField({ index: this.elseIfCount_ }), 'MINUS' + this.elseIfCount_)

    this.appendStatementInput('DO' + this.elseIfCount_);

    // Handle if-elseif-else block.
    if (this.getInput('ELSE')) {
      this.moveInputBefore("ELSETITLE", null);
      this.moveInputBefore("ELSE", null);
    }

    this.createAddButton()
  },

  removeElseIf_: function (index = undefined) {
    // The strategy for removing a part at an index is to:
    //  - Kick any blocks connected to the relevant inputs.
    //  - Move all connect blocks from the other inputs up.
    //  - Remove the last input.
    // This makes sure all of our indices are correct.

    if (index !== undefined && index != this.elseIfCount_) {
      // Each else-if is two inputs on the block:
      // the else-if input and the do input.
      const elseIfIndex = index * 2;
      const inputs = this.inputList;
      let connection = inputs[elseIfIndex].connection; // If connection.
      
      if (connection) {
        connection.disconnect();
      }
      connection = inputs[elseIfIndex + 1].connection; // Do connection.
      if (connection) {
        connection.disconnect();
      }
      this.bumpNeighbours();
      for (let i = elseIfIndex + 2, input; (input = this.inputList[i]); i++) {
        if (input.name == 'ELSE') {
          break; // Should be last, so break.
        }
        if (input.connection){
          const targetConnection = input.connection.targetConnection;
          if (targetConnection) {
            this.inputList[i - 2].connection.connect(targetConnection);
          }
        }
      }
    }

    this.removeInput('IF' + this.elseIfCount_);
    this.removeInput('IFBUTTONS' + this.elseIfCount_);
    this.removeInput('DO' + this.elseIfCount_);
    // Because else-if inputs are 1-indexed we increment first, decrement last.
    this.elseIfCount_--;
  }
};

Blockly.Blocks["logic_compare"] = {
  init: function() {
    this.appendValueInput('this');
    this.appendDummyInput('')
      .appendField(new Blockly.FieldDropdown([
          ['=', '='],
          ['!=', '!='],
          ['<', '<'],
          ['<=', '<='],
          ['>', '>'],
          ['>=', '>=']
        ]), 'operator');
    this.appendValueInput('that');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setOutputShape(1);
    this.setColour(logicColor);
  }
};

Blockly.Blocks["logic_boolean"] = {
  init: function() {
    this.appendValueInput('this');
    this.appendDummyInput('')
      .appendField(new Blockly.FieldDropdown([
          ['and', 'and'],
          ['or', 'or']
        ]), 'operator');
    this.appendValueInput('that');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setOutputShape(1);
    this.setColour(logicColor);
  }
};

Blockly.Blocks["logic_not"] = {
  init: function() {
    this.appendDummyInput('')
      .appendField('not');
    this.appendValueInput('this');
    this.setInputsInline(true)
    this.setOutput(true, null);
    this.setColour(logicColor);
  }
};