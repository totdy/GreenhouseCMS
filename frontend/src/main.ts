import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/scripts/router'

const theme = localStorage.getItem("theme");
if(theme!=null){
    document.documentElement.dataset.theme = theme;
}else{
    document.documentElement.dataset.theme = "light";
}

createApp(App).use(router).mount('#app')