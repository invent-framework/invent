import type { Component } from "vue";
import type { RouteRecordRaw } from "vue-router";

export const builderRoutes: Array<RouteRecordRaw> = [
    {
        path: "/",
        name: "Builder",
		component: async (): Promise<Component> => {
			return import ("./builder.vue");
		},
    }
]