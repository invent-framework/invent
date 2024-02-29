<template>
  <div class="h-screen w-screen flex flex-col overflow-hidden">
    <div class="h-16 py-3 px-4 w-full bg-white border-b flex items-center flex-none">
      <slot name="header" />
    </div>

    <div class="h-14 py-3 px-4 w-full bg-white border-b flex items-center flex-none">
      <slot name="toolbar" />
    </div>

    <div class="h-full w-full flex bg-gray-100 overflow-hidden">
      <div class="h-full w-72 overflow-y-auto overflow-x-hidden bg-white border-r border-gray-200 p-4 flex-none">
        <slot name="sidebar" />
      </div>

      <div class="h-full w-full flex">
        <slot name="content" />
      </div>

      <div class="h-full w-72 overflow-y-auto overflow-x-hidden bg-white border-r border-gray-200 p-4 flex-none">
        <slot name="settings" />
      </div>
    </div>
  </div>
</template>