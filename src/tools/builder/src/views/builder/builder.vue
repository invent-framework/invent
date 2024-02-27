<template>
    <builder-desktop-layout>
        <template #header>
            <ib-h-stack is-full-width :spacing="4" align-y="center" justify-content="between">
                <ib-h-stack :spacing="4">
                    <ib-h-stack :spacing="4" class="max-w-72 overflow-x-auto">
                        <ib-button 
                            v-for="(page, key) in view.state.pages" 
                            :key="key" 
                            :label="page.name" 
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
            <!-- <ib-h-stack align-y="center" justify-content="between">
                <ib-heading :label="view.getText('widgets')" size="lg" color="gray" />
                <ib-button 
                    :icon="['fas', 'plus']" 
                    size="xs"
                    @click="view.onAddWidgetClicked()" 
                />
            </ib-h-stack> -->
            <ib-v-stack :spacing="4">
                <ib-h-stack is-full-width>
                    <ib-button label="Widgets" size="sm" :color="view.getSidebarTabColor('widgets')" class="w-1/2" />
                    <ib-button label="Layout" size="sm" :color="view.getSidebarTabColor('layout')" class="w-1/2" />
                </ib-h-stack>

                <ib-v-stack :spacing="4" v-if="view.state.widgets" overflow="hidden">
                    <widget-preview 
                        v-for="widget in view.state.widgets" 
                        :key="widget.preview" 
                        :preview="widget.preview"
                        @click="view.onWidgetPreviewClicked(widget)"
                    />
                </ib-v-stack>
            </ib-v-stack>
        </template>

        <template #content>
            <page-editor class="mt-1" />
        </template>

        <template #settings>
            <ib-v-stack v-if="view.state.activeWidgetProperties" :spacing="4">
                <ib-heading label="Settings" size="lg" color="gray" />

                <template v-for="(property, key) in view.state.activeWidgetProperties" :key="key">
                    <ib-input 
                        v-if="property.property_type === 'TextProperty'" 
                        :label="key"
                        type="text"
                        :required="property.required" 
                        v-model="property.value"
                        @input="view.updateWidgetProperty(key, $event)"
                    />
                </template>
            </ib-v-stack>
        </template>
    </builder-desktop-layout> 
</template>

<script setup lang="ts">
import BuilderDesktopLayout from '@/layouts/builder-desktop-layout/builder-desktop-layout.vue';
import { view } from './builder-model';

// Components
import PageEditor from "./components/page-editor/page-editor.vue";
import WidgetPreview from "./components/widget-preview/widget-preview.vue";

view.init();
</script>