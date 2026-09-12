import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    // 允许通过内网穿透(cpolar)的域名访问开发服务器
    // 注意:true 表示放行所有域名,仅用于本地演示;生产环境要用白名单
    allowedHosts: true,
    proxy: {
      // 请求地址以 /api 开头的,都转发给后端
      '/api': {
        target: 'http://127.0.0.1:8000', // 后端地址
        changeOrigin: true,
        // 转发时把 /api 前缀去掉,变成后端真实路径(如 /api/books -> /books)
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
