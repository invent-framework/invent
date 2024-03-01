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
                            :color="view.getPageButtonColor(page)"
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
                <ib-button 
                    label="Design" 
                    size="sm" 
                    :color="view.getEditorTabColor('design')" 
                    @click="view.onEditorTabClicked('design')" 
                />
                <ib-button 
                    label="Blocks" 
                    size="sm" 
                    :color="view.getEditorTabColor('blocks')" 
                    @click="view.onEditorTabClicked('blocks')" 
                />
                <ib-button 
                    label="Get Code" 
                    size="sm" 
                    @click="view.getPythonCode()" 
                />
            </ib-h-stack>
        </template>

        <template #content >
            <div v-show="view.state.activeEditorTab === 'design'" class="h-full w-full flex">
                <div class="h-full w-72 overflow-y-auto overflow-x-hidden bg-white border-r border-gray-200 p-4 flex-none">
                    <ib-v-stack :spacing="4" v-if="view.state.widgets">
                        <widget-preview 
                            v-for="widget in view.state.widgets" 
                            :key="widget.preview" 
                            :preview="widget.preview"
                            @click="view.addWidgetToPage(widget)"
                            :draggable="true"
                            @dragstart="view.onDragStart($event, widget)"
                        />
                    </ib-v-stack>
                </div>

                <div class="h-full w-full flex">
                    <page-editor 
                        class="mt-1" 
                        :pages="view.state.pages"  
                        :activePage="view.state.activePage"
                        :add-widget-to-page="(widget: WidgetModel) => { view.addWidgetToPage(widget) }"
                    />
                </div>

                <div class="h-full w-72 overflow-y-auto overflow-x-hidden bg-white border-r border-gray-200 p-4 flex-none">
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
                </div>
            </div>

            <div v-show="view.state.activeEditorTab === 'blocks'" class="h-full w-full">
                <block-editor />
            </div>
        </template>
    </builder-desktop-layout> 
</template>

<script setup lang="ts">
import BuilderDesktopLayout from '@/layouts/builder-desktop-layout/builder-desktop-layout.vue';
import { view } from './builder-model';

// Components
import PageEditor from "./components/page-editor/page-editor.vue";
import BlockEditor from "./components/block-editor/block-editor.vue";
import WidgetPreview from "./components/widget-preview/widget-preview.vue";
import type { WidgetModel } from '@/data/models/widget-model';

view.init();
</script>