<template>
  <font-awesome-icon
    :icon="icon"
    :class="component.getClassesForIcon(size, color, backgroundColor)"
  />
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { component } from "./ib-icon-model";

defineProps<{
	icon: Array<string>;
	color?: string;
	size?: string;
	backgroundColor?: string;
}>();
</script>