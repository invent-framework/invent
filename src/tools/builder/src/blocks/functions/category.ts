import * as Blockly from 'blockly/core';

export const functionsCategory = function(workspace: any) {
    const blockList = [];

    blockList.push({
        kind: "block",
        type: "functions_define"
    });

    for (const model of Blockly.getMainWorkspace().getProcedureMap().getProcedures()) {
        console.log(model)
        blockList.push({
            kind: "block",
            type: "functions_call",
            extraState: {
                procedureId: model.getId()
            }
        })
    }

    return blockList;
}