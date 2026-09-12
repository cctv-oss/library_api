import axios from 'axios'
import { ElMessage } from 'element-plus'
import { getToken, clearAuth } from '../utils/auth'

// 统一请求工具:所有接口都从这里发出去
const request = axios.create({
  baseURL: '/api', // 由 Vite 代理转发到后端 8000
  timeout: 10000,
})

// 请求拦截器:每次发请求前,自动把 token 塞进请求头
request.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器:统一处理后端返回
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // 401 = 未登录或登录过期,清掉本地登录信息,跳回登录页
    if (error.response?.status === 401) {
      clearAuth()
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    const msg = error.response?.data?.detail || '请求失败,请检查后端服务'
    ElMessage.error(msg)
    return Promise.reject(error)
  }
)

export default request
