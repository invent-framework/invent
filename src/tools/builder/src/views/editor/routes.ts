import type { Component } from "vue";
import type { RouteRecordRaw } from "vue-router";

export const editorRoutes: Array<RouteRecordRaw> = [
    {
        path: "/",
        name: "Editor",
		component: async (): Promise<Component> => {
			return import ("./editor.vue");
		},
    }
]