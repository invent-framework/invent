<template>
  <ib-modal @close="modal.onCloseClicked()">
    <ib-modal-header
      title="Add Datastore Value"
      align="left"
      size="lg"
      @close="modal.onCloseClicked()"
    />

    <ib-modal-content>
      <ib-v-stack
        is-full-width
        :spacing="6"
        :padding-t="4"
      >
        <ib-input 
          id="firstInput" 
          v-model="modal.state.data['key']"
          :label="modal.getText('key')" 
          :placeholder="modal.getText('enter-key')"
          :error="modal.state.errors['key']" 
          type="text"
          required
          @input="modal.validateField('key')"
        />

        <ib-radio-group
          v-model="modal.state.data['type']"
          :label="modal.getText('type')"
          :options="modal.getTypeOptions()"
          required
          @input="modal.validateField('type')"
        />

        <ib-input
          v-model="modal.state.data['default_value']"
          :label="modal.getText('default-value')" 
          :placeholder="modal.getText('enter-default-value')"
          :error="modal.state.errors['default_value']" 
          :type="modal.state.data['type']"
          @input="modal.validateField('default_value')"
        />

        <ib-toggle
          v-model="modal.state.data['temporary']"
          required
          :label="modal.getText('temporary-value')"
          @input="modal.validateField('temporary')"
        />
      </ib-v-stack>
    </ib-modal-content>

    <ib-modal-footer align="right">
      <ib-button
        :label="modal.getText('add')"
        :is-disabled="!modal.state.isValid"
        @click="onAddValue(modal.state.isValid, modal.state.data)"
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
import { AddDatastoreValueModel } from "./add-datastore-value-model";

const modal: AddDatastoreValueModel = new AddDatastoreValueModel();

defineProps<{
  onAddValue: Function
}>();

onMounted(() => {
  modal.init();
})
</script>