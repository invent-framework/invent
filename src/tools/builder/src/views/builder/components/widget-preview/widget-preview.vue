

<template>
    <button class="cursor-pointer bg-gray-100 hover:bg-gray-200 transition-colors rounded-md">
        <iframe :srcdoc="getSrcDoc()" class="bg-transparent border-none p-4 pointer-events-none"></iframe>
    </button>
</template>

<script setup lang="ts">
import type { Data } from '@/components/types';

const props: Data = defineProps<{
    preview: string;
}>();

function getSrcDoc(): string {
    return `
    <link rel="stylesheet" href="https://unpkg.com/papercss@1.9.2/dist/paper.min.css">
    ${props.preview}`;
}
</script>