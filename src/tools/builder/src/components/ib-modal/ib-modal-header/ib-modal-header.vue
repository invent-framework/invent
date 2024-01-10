<template>
  <div class="px-8 pt-8 relative">
    <div class="text-center space-y-4">
      <ib-icon
        v-if="icon"
        :icon="icon"
        :color="iconColor"
        :background-color="iconColor"
      />
      <ib-heading
        :label="title"
        :size="component.getHeadingSize(size)"
        :align="align"
        is-full-width
      />
    </div>

    <div
      v-if="!isCloseHidden"
      class="absolute top-5 right-4 flex items-center"
    >
      <button
        class="h-10 w-10 rounded-md flex items-center justify-center text-gray-900 hover:bg-gray-100 cursor-pointer transition-colors dark:text-darkGray-400 dark:hover:bg-darkGray-800"
        @click="$emit('close')"
      >
        <ib-icon :icon="['fas', 'times']" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { component } from "./ib-modal-header-model";

defineProps<{
	title: string;
	align: string;
	icon?: Array<string>;
	iconColor?: string;
	size?: string;
	isCloseHidden?: boolean;
}>();

defineEmits(["close"]);
</script>