import request from './request'
import { setAuth, clearAuth } from '../utils/auth'

// 登录:成功后把 token 和用户信息存起来
export async function login(data) {
  const res = await request.post('/auth/login', data)
  setAuth(res.token, { id: res.id, name: res.name, role: res.role })
  return res
}

// 退出:只清本地,后端 token 是自带的过期机制,不用专门调接口
export function logout() {
  clearAuth()
}
