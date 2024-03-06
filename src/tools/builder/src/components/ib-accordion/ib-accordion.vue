<template>
  <div>
    <button class="bg-violet-100 px-4 py-3 space-x-3 w-full text-left" @click="component.isOpen.value = !component.isOpen.value">
      <ib-icon size="sm" :icon="component.getIcon()" />
      <span class="text-gray-700 text-sm font-medium">
        {{ label }}
      </span>
    </button>
    <div class="p-4" v-if="component.isOpen.value">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { IbAccordionModel } from "./ib-accordion-model";

const component: IbAccordionModel = new IbAccordionModel();

defineProps<{
  label: string;
}>();
</script>