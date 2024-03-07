<template>
  <div class="h-screen w-screen flex flex-col overflow-hidden">
    <div class="h-16 py-3 px-4 w-full bg-white border-b flex items-center flex-none">
      <slot name="header" />
    </div>

    <div class="h-full w-full flex bg-gray-100 overflow-hidden">
      <slot name="content" />
    </div>
  </div>
</template>