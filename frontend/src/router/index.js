import { createRouter, createWebHistory } from 'vue-router'
import Books from '../views/Books.vue'
import Readers from '../views/Readers.vue'
import Borrows from '../views/Borrows.vue'
import Login from '../views/Login.vue'
import ReaderBooks from '../views/ReaderBooks.vue'
import ReaderBorrows from '../views/ReaderBorrows.vue'
import { getToken, getUser } from '../utils/auth'

// meta.roles 表示"哪些角色能进这个页面"
const routes = [
  { path: '/login', component: Login },
  { path: '/', redirect: '/books' },
  { path: '/books', component: Books, meta: { roles: ['admin'] } },
  { path: '/readers', component: Readers, meta: { roles: ['admin'] } },
  { path: '/borrows', component: Borrows, meta: { roles: ['admin'] } },
  { path: '/reader/books', component: ReaderBooks, meta: { roles: ['reader'] } },
  { path: '/reader/borrows', component: ReaderBorrows, meta: { roles: ['reader'] } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫:每次跳转前先检查登录状态和角色
router.beforeEach((to, from, next) => {
  const token = getToken()
  const user = getUser()

  // 去登录页:如果已经登录,直接送回自己的首页
  if (to.path === '/login') {
    if (token) {
      next(user?.role === 'admin' ? '/books' : '/reader/books')
    } else {
      next()
    }
    return
  }

  // 没登录 → 一律去登录页
  if (!token) {
    next('/login')
    return
  }

  // 角色不匹配(比如读者想去管理后台)→ 送回自己该去的首页
  if (to.meta.roles && !to.meta.roles.includes(user?.role)) {
    next(user?.role === 'admin' ? '/books' : '/reader/books')
    return
  }

  next()
})

export default router
