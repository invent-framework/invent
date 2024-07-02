<template>
    <builder-desktop-layout>
        <template #header>
            <div class="w-full grid grid-cols-3">
                <ib-h-stack is-full-width align-y="center">
                    <img src="/logo.svg" class="h-7">
                </ib-h-stack>
                
                <ib-h-stack :spacing="4" is-full-width align-x="center" align-y="center">
                    <ib-h-stack :spacing="4" class="max-w-72 overflow-x-auto">
                        <ib-button
                            v-for="(page, key) in view.state.pages"
                            :key="key"
                            :label="page.properties.name"
                            size="sm"
                            :color="view.getPageButtonColor(page)"
                            @click="view.onPageClicked(page)"
                        />
                    </ib-h-stack>

                    <ib-button 
                        :icon="['fas', 'plus']" 
                        size="sm"
                        @click="view.onAddPageClicked()" 
                    />
                </ib-h-stack>

                <ib-h-stack :spacing="4" is-full-width align-x="right" align-y="center">
                    <ib-button 
                        label="Blocks" 
                        size="sm" 
                        :icon="['fas', 'puzzle-piece']"
                        :color="view.getBuilderTabColor('blocks')" 
                        @click="view.onBuilderTabClicked('blocks')"
                    />
                     
                    <ib-button 
                        label="Datastore" 
                        size="sm" 
                        :icon="['fas', 'database']"
                        :color="view.getBuilderTabColor('datastore')" 
                        @click="view.onBuilderTabClicked('datastore')"
                    />
                    
                    <ib-button 
                        label="Media" 
                        size="sm" 
                        :icon="['fas', 'image']"
                        :color="view.getBuilderTabColor('media')" 
                        @click="view.onBuilderTabClicked('media')"
                    />
                </ib-h-stack>
            </div>
        </template>

        <template #content >
            <div v-show="view.state.activeBuilderTab === 'app'" class="h-full w-full flex">
                <div v-if="view.state.widgets" class="h-full w-72 overflow-y-auto overflow-x-hidden bg-white border-r border-gray-300 flex-none divide-y divide-gray-200">
                    <ib-accordion label="Layouts">
                        <div class="grid grid-cols-2 gap-4">
                            <widget-preview 
                                v-for="container in view.state.widgets.containers" 
                                :key="container.name" 
                                :widget="container"
                                @click="view.addComponentToPage(container)"
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
                                @click="view.addComponentToPage(widget)"
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
                        :add-widget-to-page="(widget: WidgetModel) => { view.addComponentToPage(widget) }"
                    />
                </div>

                <div class="h-full w-72 overflow-y-auto overflow-x-hidden bg-white border-l border-gray-300 p-4 flex-none">
                    <ib-v-stack v-if="view.state.activeWidgetProperties" :spacing="4">
                        <ib-icon :icon="['fas', 'trash']" @click="view.deleteComponent()" class="hover:text-red-500" />
                        <div>{{ view.state.activeWidgetProperties.name.value }}</div>
                        <template v-for="(property, key) in view.state.activeWidgetProperties" :key="key">
                            <ib-h-stack is-full-width :spacing="4" align-y="center">
                                <ib-select
                                    v-if="property.is_from_datastore" 
                                    :label="key" 
                                    :options="view.getDatastoreOptions()" 
                                    v-model="property.value"
                                    @input="view.setComponentProperty(key as string, $event, property.is_layout, true)"
                                />
                                <div class="w-full" v-else>
                                    <ib-select 
                                        v-if="key === 'image'" 
                                        :label="key" 
                                        :options="view.getImageFiles()" 
                                        v-model="property.value"
                                        @input="view.setComponentProperty(key as string, $event, property.is_layout)"
                                    />

                                    <ib-select 
                                        v-else-if="key === 'source'" 
                                        :label="key" 
                                        :options="view.getSoundFiles()" 
                                        v-model="property.value"
                                        @input="view.setComponentProperty(key as string, $event, property.is_layout)"
                                    />

                                    <ib-select 
                                        v-else-if="property.property_type === 'ChoiceProperty'" 
                                        :label="key" 
                                        :options="view.getChoicePropertyOptions(property.choices)" 
                                        v-model="property.value"
                                        @input="view.setComponentProperty(key as string, $event, property.is_layout)"
                                    />

                                    <ib-toggle 
                                        v-else-if="property.property_type === 'BooleanProperty'" 
                                        :label="key" 
                                        v-model="property.value"
                                        @input="view.setComponentProperty(key as string, $event, property.is_layout)"
                                    />

                                    <ib-input 
                                        v-else
                                        :label="key"
                                        type="text"
                                        :required="property.required" 
                                        v-model="property.value"
                                        @input="view.setComponentProperty(key as string, $event, property.is_layout)"
                                    />
                                </div>

                                <ib-icon 
                                    :icon="['fas', 'database']" 
                                    color="gray" 
                                    class="hover:text-violet-500 cursor-pointer transition-colors" 
                                    :class="[property.property_type !== 'BooleanProperty' ? 'mt-6' : '', property.is_from_datastore ? '!text-violet-500' : '']" 
                                    @click="property.is_from_datastore = !property.is_from_datastore"
                                />
                            </ib-h-stack>
                        </template>
                    </ib-v-stack>

                </div>
            </div>

            <div v-show="view.state.activeBuilderTab === 'blocks'" class="h-full w-full">
                <block-editor />
            </div>

            <div v-show="view.state.activeBuilderTab === 'datastore'" class="p-8 h-full w-full">
                <div class="max-w-5xl w-full mx-auto space-y-8">
                    <ib-h-stack align-x="center" justify-content="between">
                        <ib-heading label="Datastore" size="2xl" color="gray" />

                        <ib-button label="Add" :icon="['fas', 'plus']" @click="view.onAddDatastoreValueClicked()" />
                    </ib-h-stack>

                    <ib-list v-if="Object.values(view.state.datastore).length > 0">
                        <ib-list-item 
                            v-for="value in view.state.datastore" 
                            :key="value.key" 
                            :icon="['fas', 'database']" 
                            :title="`${value.key} ${value.temporary ? '(Temporary)' : ''}`" 
                            :subtitle="`Default Value: ${value.default_value}`" 
                        />
                    </ib-list>

                    <ib-empty-state 
                        v-else
                        :title="view.getText('nothing-to-see-here')" 
                        :subtitle="view.getText('click-add')" 
                    />
                </div>
            </div>

            <div v-show="view.state.activeBuilderTab === 'media'" class="p-8 h-full w-full">
                <div class="max-w-5xl w-full mx-auto space-y-8">
                    <ib-h-stack align-x="center" justify-content="between">
                        <ib-heading label="Media" size="2xl" color="gray" />

                        <ib-button label="Add" :icon="['fas', 'plus']" @click="view.onAddMediaFile()" />
                    </ib-h-stack>

                    <ib-list v-if="Object.values(view.state.media).length > 0">
                        <ib-list-item 
                            v-for="file in view.state.media" 
                            :key="file.name" 
                            :icon="['fas', 'file']" 
                            :title="file.name" 
                            :subtitle="file.type" 
                        />
                    </ib-list>

                    <ib-empty-state 
                        v-else
                        :title="view.getText('nothing-to-see-here')" 
                        :subtitle="view.getText('click-add')" 
                    />
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