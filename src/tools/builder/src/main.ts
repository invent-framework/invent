import { createApp } from 'vue'
import App from './App.vue'
import "@/assets/tailwind.css"
import { LocalizationUtilities } from './utilities/localization-utilities'

import Components from "@/components";
import Modals from "@/modals";
import InventWidgets from "@/views/builder/components/page-editor/widgets";
import "@/data/providers/icon-provider";

// @ts-ignore
import { whenDefined } from "https://pyscript.net/releases/2024.5.1/core.js";

whenDefined("mpy").then(() => {
    LocalizationUtilities.loadPreferredLanguageAsync().then(() => {
        createApp(App)
            .use(Components)
            .use(Modals)
            .use(InventWidgets)
            .mount('#app');
    });
});
