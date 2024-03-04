

<template>
    <div class="p-4 bg-gray-100 rounded-md border text-center flex flex-col space-y-2 font-medium">
        <div v-html="widget.preview" class="text-3xl mx-auto" />
        <span>{{ widget.name }}</span>
    </div>
</template>

<script setup lang="ts">
import type { WidgetModel } from '@/data/models/widget-model';

defineProps<{
    widget: WidgetModel;
}>();
</script>