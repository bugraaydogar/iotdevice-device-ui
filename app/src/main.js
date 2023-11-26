import { createApp } from 'vue';
import App from './App.vue';
import veProgress from 'vue-ellipse-progress';
import router from './router'

import { vfmPlugin } from 'vue-final-modal';

const app = createApp(App);

app.use(vfmPlugin);
app.use(veProgress);
app.use(router)

app.mount('#app');
