<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { listBooks } from '../api/books'
import { myBorrow } from '../api/me'

const books = ref([])
const loading = ref(false)

async function loadBooks() {
  loading.value = true
  try {
    books.value = await listBooks()
  } finally {
    loading.value = false
  }
}

// 读者借书:只传图书 id,后端从登录身份里知道是谁借的
async function handleBorrow(row) {
  await myBorrow(row.id)
  ElMessage.success('借阅成功')
  loadBooks()
}

onMounted(loadBooks)
</script>

<template>
  <div>
    <h2>图书查询</h2>
    <el-table :data="books" v-loading="loading" border stripe>
      <el-table-column prop="title" label="书名" min-width="140" />
      <el-table-column prop="author" label="作者" width="120" />
      <el-table-column prop="price" label="价格" width="90" />
      <el-table-column prop="available" label="可借" width="80" />
      <el-table-column prop="publish" label="出版日期" width="120" />
      <el-table-column prop="introduction" label="简介" min-width="200" show-overflow-tooltip />
      <el-table-column label="操作" width="110" fixed="right">
        <template #default="{ row }">
          <el-button size="small" type="primary" :disabled="row.available <= 0" @click="handleBorrow(row)">
            {{ row.available > 0 ? '借阅' : '无库存' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
