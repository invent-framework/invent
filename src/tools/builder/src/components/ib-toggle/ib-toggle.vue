<template>
  <div class="flex items-center space-x-3 w-full">
    <label
      v-if="label"
      class="block text-sm font-medium text-gray-500 dark:text-darkGray-400 capitalize"
    >
      {{ label }}
      <span
        v-if="required"
        class="ml-1 text-red-500"
      >
        *
      </span>
    </label>

    <button
      class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none !ml-auto"
      :class="component.getButtonToggledClassList(modelValue)"
      @click.prevent="$emit('update:modelValue', !modelValue); $emit('input', !modelValue)"
    >
      <span
        :class="component.getToggleToggledClassList(modelValue)"
        class="pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out dark:bg-darkGray-800 dark:highlight-white/5"
      />
    </button>
  </div>
</template>

<script setup lang="ts">
import type { Data } from "../types";
import { component } from "./ib-toggle-model";

const props: Data = defineProps<{
	label?: string;
	required?: boolean;
	modelValue?: boolean;
}>();

// eslint-disable-next-line @typescript-eslint/typedef
const emit = defineEmits(["update:modelValue", "input"]);

component.init(props, emit);
</script>