import { createApp } from 'vue';
import App from './App.vue';
import veProgress from 'vue-ellipse-progress';

import { vfmPlugin } from 'vue-final-modal';

const app = createApp(App);

app.use(vfmPlugin);
app.use(veProgress);

app.mount('#app');
