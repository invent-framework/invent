<template>
    <builder-desktop-layout :header-buttons="[]">
        <template #sidebar>
            <ib-v-stack :spacing="6">
                <ib-h-stack align-y="center" justify-content="between">
                    <ib-heading :label="view.getText('pages')" />
                    <ib-button 
                        :label="view.getText('add-page')" 
                        @click="view.onAddClicked()" 
                    />
                </ib-h-stack>
                
                <ib-v-stack :spacing="2">
                    <ib-button 
                        v-for="(page, key) in view.getPages()" 
                        :key="key" 
                        :label="key" 
                        color="gray"
                        is-full-width 
                    />
                </ib-v-stack>
            </ib-v-stack>
        </template>
    </builder-desktop-layout> 
</template>

<script setup lang="ts">
import BuilderDesktopLayout from '@/layouts/builder-desktop-layout/builder-desktop-layout.vue';
import { BuilderModel } from './builder-model';

const view: BuilderModel = new BuilderModel();

view.init();
</script>