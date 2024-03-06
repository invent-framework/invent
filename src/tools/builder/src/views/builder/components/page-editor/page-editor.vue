<template>
    <div v-if="pages && activePage" class="px-4 py-3 w-full">
        <iframe 
            v-for="page in pages" 
            v-show="activePage.id === page.id"
            :key="page.name" 
            :id="`${page.id}-editor`"
            :srcdoc="component.getSrcDoc(page)" 
            class="w-full h-full"
            @load="component.onPageLoad(pages, activePage, addWidgetToPage)"
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