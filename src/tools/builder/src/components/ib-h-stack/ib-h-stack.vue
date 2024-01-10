<template>
  <div :class="component.variants({ backgroundColor, spacing, alignX, alignY, justifyContent, paddingT, paddingB, paddingL, paddingR, isFullPageHeight, isFullHeight, isFullWidth })">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { component } from "./ib-h-stack-model";

defineProps<{
	backgroundColor?: string;
	spacing?: number;
	alignX?: string;
	alignY?: string;
	justifyContent?: number;
	paddingT?: number;
	paddingB?: number;
	paddingL?: number;
	paddingR?: number;
	isFullPageHeight?: boolean;
	isFullHeight?: boolean;
	isFullWidth?: boolean;
}>();
</script>