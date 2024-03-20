import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';
import { CommonUtilities } from '@/utilities/common-utilities';
import { view as builder } from "@/views/builder/builder-model";



pythonGenerator.forBlock['summarize'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    const files: string = generator.valueToCode(block, 'files', 0);
    const summarizeId: string = CommonUtilities.getRandomId("summarize");
    const summarizeFunction: string = `
async def ${summarizeId}():
  content = await invent.read_files(${files})
  summary = await summarize(context="\\n\\n".join(content))
  return summary

`;

    builder.state.functions += summarizeFunction;
    
    const code = `await ${summarizeId}()`;
    return [code, 0];  
};

pythonGenerator.forBlock['prompt'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    const question: string = generator.valueToCode(block, 'question', 0);
    const promptFunctionId: string = CommonUtilities.getRandomId("prompt");
    const promptFunction: string = `
async def ${promptFunctionId}(question):
  filenames = invent.get_filenames()
  content = await invent.read_files(filenames)
  answer = await prompt("\\n\\n".join(content), question)
  return answer
`;

    builder.state.functions += promptFunction;

    const code = `await ${promptFunctionId}(${question})`;
    return [code, 0];
};