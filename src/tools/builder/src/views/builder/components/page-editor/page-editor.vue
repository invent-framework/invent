<template>
    <iframe id="page-editor" :srcdoc="component.getSrcDoc()" class="w-full h-full">
    </iframe>
</template>

<script setup>
import { component } from "./page-editor-model";
</script>