<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUser, clearAuth } from './utils/auth'

const route = useRoute()
const router = useRouter()

// 当前登录用户。路由变化时重新读本地存储(登录/退出后能及时更新)
const user = ref(getUser())
watch(() => route.path, () => {
  user.value = getUser()
})

const activeMenu = computed(() => route.path)

// 菜单:管理员和读者看到的不一样
const menus = computed(() => {
  if (user.value?.role === 'admin') {
    return [
      { path: '/books', label: '图书管理' },
      { path: '/readers', label: '读者管理' },
      { path: '/borrows', label: '借阅管理' },
    ]
  }
  return [
    { path: '/reader/books', label: '图书查询' },
    { path: '/reader/borrows', label: '我的借阅' },
  ]
})

function handleLogout() {
  clearAuth()
  router.push('/login')
}
</script>

<template>
  <!-- 登录页:全屏,不套后台布局 -->
  <router-view v-if="route.path === '/login'" />

  <!-- 其他页面:后台布局 -->
  <el-container v-else class="layout">
    <el-aside width="200px" class="aside">
      <div class="logo">📚 图书管理系统</div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#1f2d3d"
        text-color="#c0c4cc"
        active-text-color="#409eff"
      >
        <el-menu-item v-for="m in menus" :key="m.path" :index="m.path">{{ m.label }}</el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="user-info">
          <span>{{ user?.name }}（{{ user?.role === 'admin' ? '管理员' : '读者' }}）</span>
          <el-button size="small" @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.layout {
  height: 100%;
}
.aside {
  background-color: #1f2d3d;
}
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
}
.header {
  background: #fff;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}
.main {
  background-color: #f5f7fa;
}
</style>
