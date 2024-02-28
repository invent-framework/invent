<template>
    <iframe 
        v-for="page in pages" 
        :key="page.name" 
        :id="page.id" 
        :srcdoc="component.getSrcDoc()" 
        class="w-full h-full"
    />
</template>

<script setup lang="ts">
import type { PageModel } from "@/data/models/page-model";
import { component } from "./page-editor-model";

defineProps<{
    pages?: Array<PageModel>;
    activePage?: PageModel;
}>();
</script>