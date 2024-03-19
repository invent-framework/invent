import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "@/assets/tailwind.css"
import { LocalizationUtilities } from './utilities/localization-utilities'

import Components from "@/components";
import Modals from "@/modals";
import InventWidgets from "@/views/builder/components/page-editor/widgets";
import "@/data/providers/icon-provider";

import { whenDefined } from "https://pyscript.net/releases/2024.1.1/core.js";

whenDefined("py").then(() => {
    LocalizationUtilities.loadPreferredLanguageAsync().then(() => {
        createApp(App)
            .use(router)
            .use(Components)
            .use(Modals)
            .use(InventWidgets)
            .mount('#app');
    });
});