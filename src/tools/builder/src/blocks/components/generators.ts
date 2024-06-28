import * as Blockly from 'blockly/core';
import { PythonGenerator, pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['components_when'] = function(block: Blockly.Block, generator: PythonGenerator) {
    const component = generator.valueToCode(block, 'component', 0);
    const event = generator.valueToCode(block, 'event', 0);

    let functionBody = generator.statementToCode(block, 'function_body');
    functionBody = generator.addLoopTrap(functionBody, block) || pythonGenerator.PASS;

    const whenDecorator = `@invent.when("${event}", "${component}")`;
    const doFunction = `async def when_${component}_is_${event}(message):${functionBody}`;

    const code = `${whenDecorator}\n${doFunction}\n`;
    return code;
};
