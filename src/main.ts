import { createApp } from 'vue'
import './style.css'
import router from './utils/router.ts'
import App from './App.vue'

const app = createApp(App)
    .use(router)
app.mount('#app')


