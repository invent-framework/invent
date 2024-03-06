<template>
  <ib-modal @close="modal.onCloseClicked()">
    <ib-modal-header
      title="Published! 🎉"
      align="center"
      size="2xl"
      @close="modal.onCloseClicked()"
    />

    <ib-modal-content>
      <ib-h-stack align-y="center" class="mt-4" :spacing="4">
        <ib-input v-model="url" is-disabled />

        <ib-button label="View App" @click="modal.onViewAppClicked(url)" class="!flex-none" />
      </ib-h-stack>
    </ib-modal-content>
  </ib-modal>
</template>

<script setup lang="ts">
import type { Data } from "@/components/types";
import { AppPublishedModel } from "./app-published-model";
import { ref, type Ref } from "vue";

const modal: AppPublishedModel = new AppPublishedModel();

const props: Data = defineProps<{
  url: string;
}>();

const url: Ref<string> = ref(props.url as string);
</script>