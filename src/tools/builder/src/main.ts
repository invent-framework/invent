import { createApp } from 'vue'
import App from './app.vue'
import router from './router'
import "@/assets/tailwind.css"
import { LocalizationUtilities } from './utilities/localization-utilities'


LocalizationUtilities.loadPreferredLanguageAsync().then(() => {
    createApp(App)
        .use(router)
        .mount('#app');
});