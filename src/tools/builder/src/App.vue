<template>
  <builder />

  <!-- Modal Dynamic Component -->
  <transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <component
      :is="ModalUtilities.currentModal.value?.modal"
      v-bind="ModalUtilities.currentModal.value?.options"
    />
  </transition>
</template>

<script setup lang="ts">
import Builder from './views/builder/builder.vue';
import { ModalUtilities } from './utilities/modal-utilities';
</script>