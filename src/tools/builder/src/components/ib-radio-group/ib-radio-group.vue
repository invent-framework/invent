<template>
  <div>
    <label
      v-if="label"
      class="block text-sm font-medium text-gray-500 dark:text-darkGray-400"
    >
      {{ label }}
      <span
        v-if="required"
        class="ml-1 text-red-500"
      >
        *
      </span>
    </label>
    <div class="flex items-center space-x-6 w-full mt-2">
      <button
        v-for="option in options"
        :key="option.key"
        class="p-4 rounded-md flex-1 relative cursor-pointer text-left dark:!bg-darkGray-950"
        :class="component.getRadioButtonActiveClass(modelValue, option.key)"
        @click="$emit('update:modelValue', option.key); $emit('input', option.key)"
      >
        <ib-heading
          :label="option.title"
          color="black"
          weight="medium"
          size="sm"
        />

        <ib-heading
          v-if="option.subtitle"
          :label="option.subtitle"
          color="lightGray"
          weight="medium"
          size="sm"
        />

        <ib-icon
          v-if="modelValue === option.key"
          :icon="['fas', 'check-circle']"
          class="absolute top-4 right-4"
          color="purple"
        />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { component } from "./ib-radio-group-model";
import type { IbRadioGroupOption } from "./ib-radio-group-types";

defineProps<{
	label?: string;
	options: Array<IbRadioGroupOption>;
	modelValue: string;
	required?: boolean;
}>();

defineEmits(["update:modelValue", "input"]);
</script>