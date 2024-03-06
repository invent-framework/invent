

<template>
    <div class="p-4 bg-gray-100 rounded-md border text-center flex flex-col space-y-2 cursor-grab">
        <div v-html="widget.icon" class="text-3xl mx-auto text-violet-500" />
        <span class="text-gray-700 font-medium text-sm">{{ widget.name }}</span>
    </div>
</template>

<script setup lang="ts">
import type { WidgetModel } from '@/data/models/widget-model';

defineProps<{
    widget: WidgetModel;
}>();
</script>