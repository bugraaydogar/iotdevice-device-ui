import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import veProgress from "vue-ellipse-progress";
import { vfmPlugin } from 'vue-final-modal'


const app = createApp(App)

app.use(router)
app.use(veProgress);
app.use(vfmPlugin);

app.mount('#app')
