<template>
  <div class="h-16 w-full bg-white flex items-center justify-between flex-none px-4 border-b border-gray-200 dark:bg-darkGray-900 dark:border-darkGray-800">
    <div class="flex items-center space-x-2"></div>

    <div class="flex items-center space-x-4">
      <template
        v-for="button in buttons"
        :key="button.key"
      >
        <ib-button
          v-if="button.visible !== false"
          :label="button.label"
          :icon="button.icon"
          :color="button.color"
          size="sm"
          @click="button.action()"
        />
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
	buttons: Array<any>;
}>();
</script>