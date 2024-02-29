

<template>
    <button class="h-32 w-full p-4 bg-gray-100 hover:bg-gray-200 transition-colors rounded-md cursor-grab">
        <iframe :srcdoc="getSrcDoc()" class="h-full w-full bg-transparent pointer-events-none" />
    </button>
</template>

<script setup lang="ts">
import type { Data } from '@/components/types';

const props: Data = defineProps<{
    preview: string;
}>();

function getSrcDoc(): string {
    return `
    <head>
        <link rel="stylesheet" href="https://unpkg.com/papercss@1.9.2/dist/paper.min.css">
    </head>
    <body style="overflow:hidden;height:4.8rem;">
        ${props.preview}
    </body>`;
}
</script>