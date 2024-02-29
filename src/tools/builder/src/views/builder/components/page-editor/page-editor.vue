<template>
    <div v-if="pages && activePage" class="p-4 w-full">
        <iframe 
            v-for="page in pages" 
            v-show="activePage.id === page.id"
            :key="page.name" 
            :id="page.id" 
            :srcdoc="component.getSrcDoc()" 
            class="w-full h-full"
            @load="component.addDragAndDropEventListeners(pages, activePage, addWidgetToPage)"
        />
    </div>
</template>

<script setup lang="ts">
import type { PageModel } from "@/data/models/page-model";
import { component } from "./page-editor-model";

defineProps<{
    pages?: Array<PageModel>;
    activePage?: PageModel;
    addWidgetToPage: Function;
}>();
</script>