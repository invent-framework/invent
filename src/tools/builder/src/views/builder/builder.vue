<template>
    <builder-desktop-layout>
        <template #header>
            <ib-h-stack is-full-width :spacing="4" align-y="center" justify-content="between">
                <ib-h-stack :spacing="4">
                    <ib-h-stack :spacing="4" class="max-w-72 overflow-x-auto">
                        <ib-button 
                            v-for="(page, key) in view.getPages()" 
                            :key="key" 
                            :label="key" 
                            size="sm" 
                            color="gray" 
                            @click="view.onPageClicked(page)"
                        />
                    </ib-h-stack>

                    <ib-button 
                        :icon="['fas', 'plus']" 
                        size="xs"
                        @click="view.onAddPageClicked()" 
                    />
                </ib-h-stack>

                <ib-h-stack :spacing="4">
                    <ib-button 
                        label="App" 
                        size="sm" 
                        color="gray" 
                    />

                    <ib-button 
                        label="Datastore" 
                        size="sm" 
                        color="transparent" 
                    />

                    <ib-button 
                        label="Media" 
                        size="sm" 
                        color="transparent" 
                    />
                </ib-h-stack>
            </ib-h-stack>
        </template>

        <template #toolbar>
            <ib-h-stack is-full-width align-x="center" :spacing="4">
                <ib-button label="Design" size="sm" color="gray" />
                <ib-button label="Blocks" size="sm" color="transparent" />
            </ib-h-stack>
        </template>

        <template #sidebar>
            <ib-h-stack align-y="center" justify-content="between">
                <ib-heading :label="view.getText('widgets')" size="lg" color="gray" />
                <ib-button 
                    :icon="['fas', 'plus']" 
                    size="xs"
                    @click="view.onAddWidgetClicked()" 
                />
            </ib-h-stack>
        </template>

        <template #content>
            <page-editor />
        </template>

        <template #settings>
            <ib-heading :label="view.getText('settings')" size="lg" color="gray" />
        </template>
    </builder-desktop-layout> 
</template>

<script setup lang="ts">
import BuilderDesktopLayout from '@/layouts/builder-desktop-layout/builder-desktop-layout.vue';
import { BuilderModel } from './builder-model';

// Components
import PageEditor from "./components/page-editor/page-editor.vue";

const view: BuilderModel = new BuilderModel();

view.init();
</script>