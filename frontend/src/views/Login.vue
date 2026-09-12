<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '../api/auth'

const router = useRouter()
const role = ref('admin')     // 当前选的身份:admin / reader
const account = ref('')       // 管理员填用户名,读者填手机号
const password = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!account.value || !password.value) {
    ElMessage.warning('请填写账号和密码')
    return
  }
  loading.value = true
  try {
    await login({ account: account.value, password: password.value, role: role.value })
    ElMessage.success('登录成功')
    router.push(role.value === 'admin' ? '/books' : '/reader/books')
  } catch (e) {
    // 错误提示已经在 request.js 里统一弹过了
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-box">
      <h2>📚 图书管理系统</h2>

      <div class="role-switch">
        <el-button :type="role === 'admin' ? 'primary' : 'default'" @click="role = 'admin'">管理员</el-button>
        <el-button :type="role === 'reader' ? 'primary' : 'default'" @click="role = 'reader'">读者</el-button>
      </div>

      <el-form @submit.prevent>
        <el-form-item>
          <el-input
            v-model="account"
            :placeholder="role === 'admin' ? '用户名' : '手机号'"
            size="large"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="password"
            type="password"
            placeholder="密码"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-button type="primary" size="large" style="width: 100%" :loading="loading" @click="handleLogin">
          登 录
        </el-button>
      </el-form>

      <p class="tip">默认管理员:admin / admin123 · 读者默认密码:123456</p>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1f2d3d;
}
.login-box {
  width: 360px;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}
.login-box h2 {
  text-align: center;
  margin-bottom: 24px;
}
.role-switch {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 24px;
}
.tip {
  margin-top: 16px;
  text-align: center;
  color: #999;
  font-size: 12px;
}
</style>
