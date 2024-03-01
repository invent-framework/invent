import * as Blockly from 'blockly/core';
import { getExtraBlockState } from "./serialization-helper";

Blockly.Blocks["inline_text"] = {
    init: function(): void {
        this.appendDummyInput()
            .appendField(new Blockly.FieldTextInput(""), "value");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour("#FFFFFF");
    }
};

Blockly.Blocks["parameters"] = {
    color_: "",
    itemCount_: 0,
    minimum_: 1,
    limit_: 5,
    inputType_: undefined,
    disableCommas_: undefined,
    init: function(): void {
        this.appendDummyInput("empty");
        this.setOutput(true, "value");
        this.setInputsInline(true);
  },
  
    mutationToDom: function(): Element {
        const container: Element = Blockly.utils.xml.createElement("mutation");
        container.setAttribute("color", this.color_);
        container.setAttribute("items", this.itemCount_);
        container.setAttribute("minimum", this.minimum_);
        container.setAttribute("limit", this.limit_);
        container.setAttribute("inputType", this.inputType_);
        container.setAttribute("disableCommas", this.disableCommas_);
        return container;
    },
 
    domToMutation: function(xmlElement: HTMLElement): void {
        const targetCount: number = parseInt(xmlElement.getAttribute("items") as string, 10);
        this.color_ = xmlElement.getAttribute("color");
        this.minimum_ = parseInt(xmlElement.getAttribute("minimum") as string, 10) || 1; 
        this.limit_ = parseInt(xmlElement.getAttribute("limit") as string, 10);
        this.inputType_ = xmlElement.getAttribute("inputType");
        this.disableCommas_ = xmlElement.getAttribute("disableCommas");
        this.setColour(this.color_);
        this.updateShape_(targetCount);
    },

    getAttributes(): object {
        return {
            "color": this.color_,
            "minimum": this.minimum_,
            "limit": this.limit_,
            "inputType": this.inputType_,
            "disableCommas": this.disableCommas_,
        };
    },

    saveExtraState: function(): object {
        return {
            "itemCount": this.itemCount_
        };
    },

    loadExtraState: function(state: any): void {
        this.updateShape_(state["itemCount"]);
    },
  
    updateShape_: function(targetCount: number): void {
        while (this.itemCount_ < targetCount) {
            this.addPart_();
        }
        while (this.itemCount_ > targetCount) {
            this.removePart_();
        }
        this.updateMinus_();
        this.updatePlus_();
    },
 
    plus: function(): void {
        this.addPart_();
        this.updateMinus_();
        this.updatePlus_();
    },
  
    minus: function(): void {
        if (this.itemCount_ === 0) {
            return;
        }
        this.removePart_();
        this.updateMinus_();
        this.updatePlus_();
    },

    createPlusField: function(args: any = undefined): Blockly.Field {
        const plus: any = new Blockly.FieldImage("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTMiIHZpZXdCb3g9IjAgMCAxMiAxMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTUuNDM3NSA4LjU2MjVWNy4wNjI1SDMuOTM3NUMzLjYwOTM4IDcuMDYyNSAzLjM3NSA2LjgyODEyIDMuMzc1IDYuNUMzLjM3NSA2LjE5NTMxIDMuNjA5MzggNS45Mzc1IDMuOTM3NSA1LjkzNzVINS40Mzc1VjQuNDM3NUM1LjQzNzUgNC4xMzI4MSA1LjY3MTg4IDMuODc1IDYgMy44NzVDNi4zMDQ2OSAzLjg3NSA2LjU2MjUgNC4xMzI4MSA2LjU2MjUgNC40Mzc1VjUuOTM3NUg4LjA2MjVDOC4zNjcxOSA1LjkzNzUgOC42MjUgNi4xOTUzMSA4LjYyNSA2LjVDOC42MjUgNi44MjgxMiA4LjM2NzE5IDcuMDYyNSA4LjA2MjUgNy4wNjI1SDYuNTYyNVY4LjU2MjVDNi41NjI1IDguODkwNjIgNi4zMDQ2OSA5LjEyNSA2IDkuMTI1QzUuNjcxODggOS4xMjUgNS40Mzc1IDguODkwNjIgNS40Mzc1IDguNTYyNVpNMTIgNi41QzEyIDkuODI4MTIgOS4zMDQ2OSAxMi41IDYgMTIuNUMyLjY3MTg4IDEyLjUgMCA5LjgyODEyIDAgNi41QzAgMy4xOTUzMSAyLjY3MTg4IDAuNSA2IDAuNUM5LjMwNDY5IDAuNSAxMiAzLjE5NTMxIDEyIDYuNVpNNiAxLjYyNUMzLjMwNDY5IDEuNjI1IDEuMTI1IDMuODI4MTIgMS4xMjUgNi41QzEuMTI1IDkuMTk1MzEgMy4zMDQ2OSAxMS4zNzUgNiAxMS4zNzVDOC42NzE4OCAxMS4zNzUgMTAuODc1IDkuMTk1MzEgMTAuODc1IDYuNUMxMC44NzUgMy44MjgxMiA4LjY3MTg4IDEuNjI1IDYgMS42MjVaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K", 20, 20, undefined, this.onPlusFieldClicked);
        plus.args_ = args;
        return plus;
    },

    onPlusFieldClicked: function(plusField: any): void {
        const block: any = plusField.getSourceBlock();

        if (!block.isInFlyout) {
            Blockly.Events.setGroup(true);
            const oldExtraState: string | undefined = getExtraBlockState(block);
            block.plus(plusField.args_);
            const newExtraState: string | undefined = getExtraBlockState(block);
            if (oldExtraState !== newExtraState) {
                Blockly.Events.fire(new Blockly.Events.BlockChange(block, "mutation", undefined, oldExtraState, newExtraState));
            }
            Blockly.Events.setGroup(false);
        }
    },

    createMinusField: function(args: any = undefined): Blockly.Field {
        const minus: any = new Blockly.FieldImage("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTMiIHZpZXdCb3g9IjAgMCAxMiAxMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTguMDYyNSA1LjkzNzVDOC4zNjcxOSA1LjkzNzUgOC42MjUgNi4xOTUzMSA4LjYyNSA2LjVDOC42MjUgNi44MjgxMiA4LjM2NzE5IDcuMDYyNSA4LjA2MjUgNy4wNjI1SDMuOTM3NUMzLjYwOTM4IDcuMDYyNSAzLjM3NSA2LjgyODEyIDMuMzc1IDYuNUMzLjM3NSA2LjE5NTMxIDMuNjA5MzggNS45Mzc1IDMuOTM3NSA1LjkzNzVIOC4wNjI1Wk0xMiA2LjVDMTIgOS44MjgxMiA5LjMwNDY5IDEyLjUgNiAxMi41QzIuNjcxODggMTIuNSAwIDkuODI4MTIgMCA2LjVDMCAzLjE5NTMxIDIuNjcxODggMC41IDYgMC41QzkuMzA0NjkgMC41IDEyIDMuMTk1MzEgMTIgNi41Wk02IDEuNjI1QzMuMzA0NjkgMS42MjUgMS4xMjUgMy44MjgxMiAxLjEyNSA2LjVDMS4xMjUgOS4xOTUzMSAzLjMwNDY5IDExLjM3NSA2IDExLjM3NUM4LjY3MTg4IDExLjM3NSAxMC44NzUgOS4xOTUzMSAxMC44NzUgNi41QzEwLjg3NSAzLjgyODEyIDguNjcxODggMS42MjUgNiAxLjYyNVoiIGZpbGw9IndoaXRlIi8+Cjwvc3ZnPgo=", 20, 20, undefined, this.onMinusFieldClicked);
        minus.args_ = args;
        return minus;
    },

    onMinusFieldClicked: function(minusField: any): void {
        const block: any = minusField.getSourceBlock();

        if (!block.isInFlyout) {
            Blockly.Events.setGroup(true);
            const oldExtraState: string | undefined = getExtraBlockState(block);
            block.minus(minusField.args_);
            const newExtraState: string | undefined = getExtraBlockState(block);
            if (oldExtraState !== newExtraState) {
                Blockly.Events.fire(new Blockly.Events.BlockChange(block, "mutation", undefined, oldExtraState, newExtraState));
            }
            Blockly.Events.setGroup(false);
        }
    },

    addPart_: function(): void {
        if (this.itemCount_ === 0) {
            this.removeInput("empty");
            if (this.minimum_ !== this.limit_) {
                this.topInput_ = this.appendValueInput(`input_${this.itemCount_ + 1}`)
                    .appendField(this.createPlusField(), "plus_icon");
            }
            else {
                this.topInput_ = this.appendValueInput(`input_${this.itemCount_ + 1}`);
            }
            this.addShadowBlock(this.topInput_);
      }
        else {
            let input: Blockly.Input;
            if (this.disableCommas_ === "true") {
                input = this.appendValueInput(`input_${this.itemCount_ + 1}`);
            }
            else {
                input = this.appendValueInput(`input_${this.itemCount_ + 1}`)
                    .appendField(", ");
            }
            this.addShadowBlock(input);
      }
      this.itemCount_++;
    },

    addShadowBlock: function(input: Blockly.Input): void {
        const sourceBlock: Blockly.Block = input.getSourceBlock();
        if (!sourceBlock.isInFlyout) {
            const shadowBlock: Blockly.BlockSvg = Blockly.getMainWorkspace().newBlock("inline_text") as unknown as Blockly.BlockSvg;
            shadowBlock.setShadow(true);
            shadowBlock.initSvg();
            shadowBlock.render();
            input.connection!.connect(shadowBlock.outputConnection);
        }
    },

    removePart_: function(): void {
        this.itemCount_--;
        this.removeInput(`input_${this.itemCount_ + 1}`);
        if (this.itemCount_ === 0 && (this.minimum_ !== this.limit_)) {
            this.topInput_ = this.appendDummyInput("empty")
                .appendField(this.createPlusField(), "plus_icon");
        }
    },

    updatePlus_: function(): void {
        const plusField: Blockly.Field = this.getField("plus_icon");
        if (!plusField && this.itemCount_ > 0 && (this.minimum_ !== this.limit_)) {
            this.topInput_.insertFieldAt(0, this.createPlusField(), "plus_icon");
        }
        else if (plusField && this.itemCount_ === this.limit_) {
            this.topInput_.removeField("plus_icon");
        }
    },

    updateMinus_: function(): void {
        const minusField: Blockly.Field = this.getField("minus_icon");
        if (!minusField && this.itemCount_ > 0) {
            if (this.minimum_ !== this.limit_ && this.itemCount_ !== this.minimum_) {
                this.topInput_.insertFieldAt(1, this.createMinusField(), "minus_icon");
            }
        }
        else if (minusField && this.itemCount_ < 2) {
            this.topInput_.removeField("minus_icon");
        }
    }
};