<template>
  <div class="h-screen w-screen bg-gray-100 flex flex-col overflow-hidden dark:bg-darkGray-950">
    <div class="py-3 px-4 w-full bg-white border-b flex items-center flex-none">
      <slot name="header" />
    </div>

    <div class="h-16 px-4 w-full bg-white flex items-center border-b over">
      <slot name="toolbar" />
    </div>
    
    <div class="h-full w-full flex overflow-hidden">
      <div class="h-full w-72 bg-white border-r border-gray-200 flex-none p-4">
        <slot name="sidebar" />
      </div>

      <div class="h-full w-full flex ">
        <slot name="content" />
      </div>

      <div class="h-full w-72 bg-white border-r border-gray-200 flex-none p-4">
        <slot name="settings" />
      </div>
    </div>
  </div>
</template>