<template>
    <div id="block-editor" class="h-full w-full" />
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { component } from "./block-editor-model";

onMounted(() => {
    component.init();
});
</script>

<style lang="postcss">
.blocklyToolboxDiv {
    @apply bg-white border-r;
}

.blocklyMainBackground {
    @apply stroke-0;
}

.blocklyTreeRow {
    @apply !p-2 w-full h-full flex items-center cursor-pointer transition-all !mb-1;
}

.blocklyTreeRow:not(.blocklyTreeSelected) {
    @apply hover:!bg-gray-100;
} 

.blocklySvg {
    @apply border-none rounded-none bg-gray-100;
}

.blocklyTreeLabel {
    @apply text-gray-700 font-sans font-medium;
}

.blocklyFlyoutButton {
    @apply fill-violet-500 hover:!fill-violet-400 transition-colors;
}

.blocklyFlyoutButtonBackground {
    @apply stroke-violet-500;
}

.blocklyFlyoutButton .blocklyText {
    @apply !text-sm !font-sans !font-medium cursor-pointer;
}

.zelos-renderer.classic-theme .blocklyText, .zelos-renderer.classic-theme .blocklyFlyoutLabelText {
    @apply !font-sans !font-semibold;
}
</style>