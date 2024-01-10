<template>
    <builder-desktop-layout :header-buttons="[]">
        <template #sidebar>
            <ib-button label="Add" @click="" />
        </template>
    </builder-desktop-layout> 
</template>

<script setup lang="ts">
import BuilderDesktopLayout from '@/layouts/builder-desktop-layout/builder-desktop-layout.vue';
import { EditorModel } from './editor-model';

const view: EditorModel = new EditorModel();
</script>