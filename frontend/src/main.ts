import { createApp } from "vue"
import App from "@/App.vue"
import router from "@/scripts/router"

import { locales } from "@/localization"
import { createI18n } from "vue-i18n"

const locale = localStorage.getItem("locale") ?? "en";
const i18n = createI18n({
    legacy: false,
    fallbackLocale: "en",
    locale: locale,
    messages: locales,
})

const theme = localStorage.getItem("theme") ?? "light"
document.documentElement.dataset.theme = theme

createApp(App).use(router).use(i18n).mount("#app")