import { createApp } from "vue"
import App from "@/App.vue"
import router from "@/scripts/router"

import { locales } from "@/localization"
import { createI18n } from "vue-i18n"

const i18n = createI18n({
    legacy: false,
    fallbackLocale: "en",
    locale: "en",
    messages: locales,
})

const theme = localStorage.getItem("theme");
if(theme!=null){
    document.documentElement.dataset.theme = theme;
}else{
    document.documentElement.dataset.theme = "light";
}

createApp(App).use(router).use(i18n).mount("#app")