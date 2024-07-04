import * as Blockly from 'blockly/core';
import { PythonGenerator, pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['widgets_widgets'] = function(block: Blockly.Block) {
    const widget: string = block.getFieldValue('widget');
    const code = widget;
    return [code, 0];  
};

pythonGenerator.forBlock['widgets_events'] = function(block: Blockly.Block) {
    const event: string = block.getFieldValue('event');
    const code = event;
    return [code, 0];  
};

pythonGenerator.forBlock['widgets_when'] = function(block: Blockly.Block, generator: PythonGenerator) {
    const widget = generator.valueToCode(block, 'widget', 0);
    const event = generator.valueToCode(block, 'event', 0);

    let functionBody = generator.statementToCode(block, 'function_body');
    functionBody = generator.addLoopTrap(functionBody, block) || pythonGenerator.PASS;

    const whenDecorator = `@invent.when("${event}", "${widget}")`;
    const doFunction = `async def when_${widget.replaceAll("-", "_")}_is_${event}(message):\n${functionBody}`;

    const code = `${whenDecorator}\n${doFunction}\n`;
    return code;
};
