<template>
  <div class="w-full flex items-center space-x-4 rounded-md p-2 hover:bg-gray-50 transition-colors">
	<div class="bg-gray-100 rounded-md h-10 w-10 flex items-center justify-center">
		<ib-icon :icon="icon" color="purple" />
	</div>

	<div>
		<ib-heading
			:label="title"
			color="black"
			size="sm"
			weight="medium"
		/>

		<ib-heading
			:label="subtitle"
			color="lightGray"
			size="xs"
			weight="normal"
		/>
	</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
	icon?: Array<string>;
	title?: string;
	subtitle?: string;
}>();
</script>