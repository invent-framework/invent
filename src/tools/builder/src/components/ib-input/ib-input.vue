<template>
  <div class="w-full">
    <label
      v-if="label"
      class="block text-sm font-medium text-gray-500 mb-2 dark:text-darkGray-400 capitalize"
    >
      {{ label }}
      <span
        v-if="required"
        class="ml-1 text-red-500"
      >
        *
      </span>
    </label>
    <div class="w-full">
      <input
        :id="id"
        :type="type"
        :tabindex="tabindex"
        class="block w-full rounded-md border-none bg-gray-100 focus:ring-gray-300 focus:outline-none px-3 py-2.5 text-sm dark:bg-darkGray-950 dark:highlight-white/5 dark:text-darkGray-200 dark:focus:ring-gray-800 dark:placeholder:text-gray-400"
        :class="error ? 'border-red-500' : 'border-gray-300'"
        :placeholder="placeholder"
        :disabled="isDisabled"
        :value="modelValue"
        @input="component.updateModelValue($event, $emit)"
      >
    </div>
    <a
      v-if="error"
      class="text-sm text-red-500 font-medium mt-1"
    >
      {{ error }}
    </a>
  </div>
</template>

<script setup lang="ts">
import { component } from "./ib-input-model";

defineProps<{
  id?: string;
	label?: string;
  tabindex?: string;
	type: string;
	placeholder?: string;
	modelValue?: string;
	required?: boolean;
	isDisabled?: boolean;
	error?: string;
}>();

defineEmits(["update:modelValue", "input"]);
</script>