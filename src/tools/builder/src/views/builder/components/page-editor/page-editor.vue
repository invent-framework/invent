<template>
    {{ component.getActivePage() }}
</template>

<script setup lang="ts">
import { PageEditorModel } from './page-editor-model';

const component: PageEditorModel = new PageEditorModel();
</script>