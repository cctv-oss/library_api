// 登录状态管理:把 token 和用户信息存在浏览器本地(localStorage)
const TOKEN_KEY = 'library_token'
const USER_KEY = 'library_user'

// 登录成功后调用:保存通行证 + 用户信息
export function setAuth(token, user) {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

// 取出通行证
export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

// 取出当前用户信息
export function getUser() {
  const u = localStorage.getItem(USER_KEY)
  return u ? JSON.parse(u) : null
}

// 退出登录:清掉本地保存的登录信息
export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}
