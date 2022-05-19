import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import veProgress from "vue-ellipse-progress";


const app = createApp(App)

app.use(router)
app.use(veProgress);


app.mount('#app')
