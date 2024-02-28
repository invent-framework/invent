<template>
  <ib-modal @close="modal.onCloseClicked()">
    <ib-modal-header
      :title="modal.getText('add-page')"
      align="left"
      size="lg"
      @close="modal.onCloseClicked()"
    />

    <ib-modal-content>
      <ib-input 
        id="firstInput" 
        v-model="modal.state.data['name']"
        :label="modal.getText('name')" 
        :placeholder="modal.getText('enter-page-name')"
        :error="modal.state.errors['name']" 
        type="text"
        required
        @input="modal.validateField('name')"
      />
    </ib-modal-content>

    <ib-modal-footer align="right">
      <ib-button
        :label="modal.getText('add')"
        @click="onAddPage(modal.state.data['name'])"
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
import { AddPageModel } from "./add-page-model";

const modal: AddPageModel = new AddPageModel();

defineProps<{
  onAddPage: Function
}>();

onMounted(() => {
  modal.init();
})
</script>