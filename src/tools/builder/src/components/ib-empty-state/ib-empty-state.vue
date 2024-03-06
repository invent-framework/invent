<template>
  <div :class="component.variants({ isFullHeight, isFullWidth, backgroundColor })">
    <div class="py-8 px-4">
      <ib-icon
        v-if="icon"
        :icon="icon"
        size="4xl"
        color="gray"
        class="w-full mb-4"
      />

      <ib-heading
        :label="title"
        size="sm"
        color="black"
        weight="semibold"
        align="center"
      />

      <ib-heading
        v-if="subtitle"
        :label="subtitle"
        size="sm"
        color="lightGray"
        weight="normal"
        class="mt-1"
        align="center"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { component } from "./ib-empty-state-model";

defineProps<{
	title: string;
	subtitle?: string;
	icon?: Array<string>;
	backgroundColor?: string;
	isFullHeight?: boolean;
	isFullWidth?: boolean;
}>();
</script>