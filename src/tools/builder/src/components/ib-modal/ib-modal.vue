<template>
  <div>
    <!-- Overlay -->
    <div
      class="absolute inset-0 h-screen w-screen bg-gray-900/40 z-[200] dark:bg-darkGray-400/40"
      @click="$emit('close')"
    />

    <!-- Modal -->
    <div class="absolute inset-0 h-screen w-screen p-2 md:p-10 flex items-center justify-center z-[300] pointer-events-none">
      <div class="max-h-full flex flex-col max-w-2xl w-full bg-white rounded-md pointer-events-auto overflow-hidden dark:bg-darkGray-900">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineEmits(["close"]);
</script>