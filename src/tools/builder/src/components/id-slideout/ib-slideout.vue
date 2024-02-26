<template>
  <!-- Overlay -->
  <transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
  <div
    v-if="visible"
    class="absolute inset-0 h-screen w-screen bg-gray-900/40 z-0 dark:bg-darkGray-400/40"
    @click="$emit('close')"
  />
  </transition>

  <transition enter-active-class="transform transition ease-in-out duration-300" enter-from-class="-translate-x-full" enter-to-class="-translate-x-0" leave-active-class="transform transition ease-in-out duration-300" leave-from-class="-translate-x-0" leave-to-class="-translate-x-full">
    <div v-if="visible" class="absolute h-full w-full inset-0 p-4 flex items-center pointer-events-none">
      <div class="h-full w-full max-w-sm bg-white rounded-xl z-50 p-6 pointer-events-auto">
        <slot />
      </div>
    </div>
  </transition>

</template>

<script setup lang="ts">
defineProps<{
  visible: boolean;
}>();

defineEmits(["close"]);
</script>