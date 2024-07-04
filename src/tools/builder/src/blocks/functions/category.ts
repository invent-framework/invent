import * as Blockly from 'blockly/core';

export const functionsCategory = function(workspace: any) {
    const blockList = [];

    blockList.push({
        kind: "block",
        type: "functions_define"
    });

    for (const model of workspace.getProcedureMap().getProcedures()) {
        console.log(model);
        blockList.push({
            kind: "block",
            type: "functions_call",
            extraState: {
                name: model.getName()
            }
        })
    }

    return blockList;
}