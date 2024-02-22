<template>
  <ib-modal @close="modal.onCloseClicked()">
    <ib-modal-header
      :title="modal.getText('add-content')"
      align="left"
      size="lg"
      @close="modal.onCloseClicked()"
    />

    <ib-modal-content>
      <ib-input id="firstInput" label="Test" />
    </ib-modal-content>

    <ib-modal-footer align="right">
      <ib-button
        :label="modal.getText('submit')"
        color="purple"
      />

      <ib-button
        :label="modal.getText('cancel')"
        color="white"
        @click="modal.onCloseClicked()"
      />
    </ib-modal-footer>
  </ib-modal>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { modal } from "./add-widget-model";

onMounted(() => {
  modal.init();
})
</script>