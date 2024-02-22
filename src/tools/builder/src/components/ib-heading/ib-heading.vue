<template>
  <h1 :class="component.variants({ align, size, weight, color, isFullWidth })">
    {{ label }}
  </h1>
</template>

<script setup lang="ts">
import { component } from "./ib-heading-model";

defineProps<{
	label: string;
	align?: string;
	size?: string;
	weight?: string;
	color?: string;
	isFullWidth?: boolean;
}>();
</script>