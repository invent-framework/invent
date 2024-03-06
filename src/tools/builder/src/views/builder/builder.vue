<template>
    <builder-desktop-layout>
        <template #header>
            <ib-h-stack is-full-width :spacing="4" align-y="center">
                <img src="/logo.svg" class="h-7">

                <ib-h-stack v-show="view.state.activeBuilderTab === 'app'" :spacing="4">
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

                <ib-h-stack :spacing="4" class="!ml-auto">
                    <ib-button 
                        label="App" 
                        size="sm" 
                        :color="view.getBuilderTabColor('app')" 
                        @click="view.onBuilderTabClicked('app')"
                    />
                     
                    <ib-button 
                        label="Datastore" 
                        size="sm" 
                        :color="view.getBuilderTabColor('datastore')" 
                        @click="view.onBuilderTabClicked('datastore')"
                    />
                    
                    <ib-button 
                        label="Media" 
                        size="sm" 
                        :color="view.getBuilderTabColor('media')" 
                        @click="view.onBuilderTabClicked('media')"
                    />

                    <ib-button 
                        label="Publish" 
                        size="sm" 
                        :is-loading="view.state.isPublishing"
                        :icon="['fas', 'rocket']"
                        @click="view.getPythonCode()" 
                    />
                </ib-h-stack>
            </ib-h-stack>
        </template>
        
        <template #toolbar>
            <ib-h-stack v-show="view.state.activeBuilderTab === 'app'" is-full-width align-x="center" :spacing="4">
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
            </ib-h-stack>
        </template>

        <template #content >
            <div v-show="view.state.activeBuilderTab === 'app' && view.state.activeEditorTab === 'design'" class="h-full w-full flex">
                <div v-if="view.state.widgets" class="h-full w-72 overflow-y-auto overflow-x-hidden bg-white border-r border-gray-200 flex-none divide-y divide-gray-200">
                    <ib-accordion label="Containers">
                        <div class="grid grid-cols-2 gap-4">
                            <widget-preview 
                                v-for="container in view.state.widgets.containers" 
                                :key="container.name" 
                                :widget="container"
                                @click="view.addWidgetToPage(container)"
                                :draggable="true"
                                @dragstart="view.onDragStart($event, container)"
                            />
                        </div>
                    </ib-accordion>
                    
                    <ib-accordion label="Widgets">
                        <div class="grid grid-cols-2 gap-4">
                            <widget-preview 
                                v-for="widget in view.state.widgets.widgets" 
                                :key="widget.name" 
                                :widget="widget"
                                @click="view.addWidgetToPage(widget)"
                                :draggable="true"
                                @dragstart="view.onDragStart($event, widget)"
                            />
                        </div>
                    </ib-accordion>
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
                            <ib-select 
                                v-if="key === 'image'" 
                                :label="key" 
                                :options="view.getImageFiles()" 
                            />

                            <ib-input 
                                v-else
                                :label="key"
                                type="text"
                                :required="property.required" 
                                v-model="property.value"
                                @input="view.updateWidgetProperty(key as string, $event)"
                            />
                        </template>
                    </ib-v-stack>

                </div>
            </div>

            <div v-show="view.state.activeBuilderTab === 'app' && view.state.activeEditorTab === 'blocks'" class="h-full w-full">
                <block-editor />
            </div>

            <div v-show="view.state.activeBuilderTab === 'datastore'" class="p-8 h-full w-full">
                <div class="max-w-5xl w-full mx-auto space-y-8">
                    <ib-h-stack align-x="center" justify-content="between">
                        <ib-heading label="Datastore" size="2xl" color="gray" />

                        <ib-button label="Add" :icon="['fas', 'plus']" @click="view.onAddDatastoreValueClicked()" />
                    </ib-h-stack>

                    <ib-list>
                        <ib-list-item 
                            v-for="value in view.state.datastore" 
                            :key="value.key" 
                            :icon="['fas', 'database']" 
                            :title="`${value.key} ${value.temporary ? '(Temporary)' : ''}`" 
                            :subtitle="`Default Value: ${value.default_value}`" 
                        />
                    </ib-list>
                </div>
            </div>

            <div v-show="view.state.activeBuilderTab === 'media'" class="p-8 h-full w-full">
                <div class="max-w-5xl w-full mx-auto space-y-8">
                    <ib-h-stack align-x="center" justify-content="between">
                        <ib-heading label="Media" size="2xl" color="gray" />

                        <ib-button label="Upload" :icon="['fas', 'file-upload']" @click="view.uploadMediaFile()" />
                    </ib-h-stack>

                    <ib-list>
                        <ib-list-item 
                            v-for="file in view.state.media" 
                            :key="file.name" 
                            :icon="['fas', 'file']" 
                            :title="file.name" 
                            :subtitle="file.type" 
                        />
                    </ib-list>
                </div>
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