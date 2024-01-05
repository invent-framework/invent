<template>
    <h1 class="text-red-500">{{ view.getText("editor") }}</h1>
</template>

<script setup lang="ts">
import { EditorModel } from './editor-model';

const view: EditorModel = new EditorModel();
</script>