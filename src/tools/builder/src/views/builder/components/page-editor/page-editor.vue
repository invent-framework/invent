<template>
    <draggable v-if="component.activePage.value" :list="component.activePage.value.container.children">
        <template #item="{element}">
            <div class="w-full">
                <component :is="`invent-${element.type}`" />
            </div>
          </template>
    </draggable>
</template>

<script setup lang="ts">
import { PageEditorModel } from './page-editor-model';
import draggable from "vuedraggable";

const component: PageEditorModel = new PageEditorModel();
</script>