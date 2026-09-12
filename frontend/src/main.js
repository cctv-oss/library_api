import { createApp } from 'vue'
import ElementPlus from 'element-plus'      // UI 组件库(表格、按钮、菜单等)
import 'element-plus/dist/index.css'        // Element Plus 自带的样式
import App from './App.vue'
import router from './router'               // 路由配置

import './style.css'

const app = createApp(App)
app.use(ElementPlus)  // 登记:让整个项目都能用 Element Plus 组件
app.use(router)       // 登记:让整个项目都能用路由跳转
app.mount('#app')
