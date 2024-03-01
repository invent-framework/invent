import { CommonUtilities } from '@/utilities/common-utilities';
import * as Blockly from 'blockly/core';
import { pythonGenerator } from 'blockly/python';

pythonGenerator.forBlock['subscribe'] = function(block: Blockly.Block, generator: Blockly.Generator) {
    let onSubject = generator.statementToCode(block, "on_subject");
	onSubject = generator.addLoopTrap(onSubject, block) || pythonGenerator.PASS;

    const channels: string = generator.valueToCode(block, 'channels', 0);
    const channelsArray: Array<string> = channels.split(",").map((channel: string) => {
        return channel.trim();
    });

    const subjects: string = generator.valueToCode(block, 'subjects', 0);
    const subjectsArray: Array<string> = subjects.split(",").map((subject: string) => {
        return subject.trim();
    });

    const onSubjectDefinitionId: string = CommonUtilities.getRandomId("subscribe");
    const onSubjectDefinition: string = `def ${onSubjectDefinitionId}():\n${onSubject}\n`;
    const subscribe: string = `invent.subscribe(${onSubjectDefinitionId}, to_channel=${JSON.stringify(channelsArray)}, when_subject=${JSON.stringify(subjectsArray)})`;

    const code = `${onSubjectDefinition}\n${subscribe}\n`;
    return code;  
};
  