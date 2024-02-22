<template>
  <button :class="component.variants({ align, size, color, isFullWidth, isDisabled })">
    <template v-if="!isLoading">
      <ib-icon
        v-if="icon"
        :icon="icon"
        :color="component.getIconColor(color, isDisabled)"
        class="text-lg fa-fw"
        :class="label ? '-ml-1 mr-3' : ''"
      />
      <img
        v-if="image"
        :src="image"
        class="h-4"
        :class="label ? '-ml-1 mr-3' : ''"
      >
      <span v-if="label">{{ label }}</span>
    </template>
    <template v-else>
      <svg
        class="animate-spin h-5 w-5 text-white"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        />
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
    </template>
  </button>
</template>

<script setup lang="ts">
import { component } from "./ib-button-model";

defineProps<{
	label?: string;
	icon?: Array<string>;
	image?: string;
	align?: string;
	size?: string;
	color?: string;
	isLoading?: boolean;
	isFullWidth?: boolean;
	isDisabled?: boolean;
}>();
</script>