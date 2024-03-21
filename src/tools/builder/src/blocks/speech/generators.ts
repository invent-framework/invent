import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';
import { CommonUtilities } from '@/utilities/common-utilities';
import { view as builder } from "@/views/builder/builder-model";



pythonGenerator.forBlock['say'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    const text: string = generator.valueToCode(block, 'text', 0);
    // const summarizeId: string = CommonUtilities.getRandomId("summarize");
//     const summarizeFunction: string = `
// async def ${summarizeId}():
//   content = await invent.read_files(${files})
//   summary = await summarize(context="\\n\\n".join(content))
//   return summary

// `;

    // builder.state.functions += summarizeFunction;
    
    const code = `invent.say(${text})`;
    return code;
};


pythonGenerator.forBlock['listen'] = function(block: Blockly.Block, generator: Blockly.Generator) {
//   const summarizeId: string = CommonUtilities.getRandomId("listen");
//   const summarizeFunction: string = `
// async def ${summarizeId}():
//   content = await invent.read_files()
//   summary = await summarize(context="\\n\\n".join(content))
//   return summary

// `;

//     builder.state.functions += summarizeFunction;
    const code = `await invent.listen()`;
    return [code, 0];  
};


pythonGenerator.forBlock['set_voice'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    const value: string = generator.valueToCode(block, 'value', 0);
    const code = `invent.set_voice(${value})\n`;
    return code;
};
