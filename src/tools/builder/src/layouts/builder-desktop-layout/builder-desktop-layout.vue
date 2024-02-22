<template>
  <div class="h-screen w-screen bg-gray-100 flex flex-col overflow-hidden dark:bg-darkGray-950">
    <div class="py-3 px-4 w-full bg-white border-b flex items-center flex-none">
      <slot name="header" />
    </div>

    <div class="h-16 px-4 w-full bg-white flex items-center border-b">
      <slot name="toolbar" />
    </div>
    
    <div class="h-full w-full flex overflow-hidden">
      <div class="h-full w-72 bg-white border-r border-gray-200 flex-none p-4">
        <slot name="sidebar" />
      </div>

      <div class="h-full w-full flex">
        <div
          class="relative h-full w-full flex flex-col overflow-y-auto"
          @scroll="$emit('scroll', $event)"
        >
          <div class="w-full p-10 max-w-5xl mx-auto space-y-8">
            <slot name="content" />
          </div>
        </div>

        <div class="h-full bg-white border-l border-gray-200">
          <slot name="context" />
        </div>
      </div>

      <div class="h-full w-72 bg-white border-r border-gray-200 flex-none p-4">
        <slot name="settings" />
      </div>
    </div>
  </div>
</template>