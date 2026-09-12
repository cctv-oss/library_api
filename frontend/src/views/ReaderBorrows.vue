<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listBooks } from '../api/books'
import { myBorrows, myReturn } from '../api/me'

const borrows = ref([])
const books = ref([])
const loading = ref(false)

function bookTitle(id) {
  const b = books.value.find((x) => x.id === id)
  return b ? b.title : `#${id}`
}

function statusInfo(status) {
  if (status === 'borrowed') return { text: '借阅中', type: 'warning' }
  if (status === 'returned') return { text: '已归还', type: 'success' }
  if (status === 'overdue') return { text: '逾期归还', type: 'danger' }
  return { text: status, type: 'info' }
}

async function loadData() {
  loading.value = true
  try {
    const [bList, bookList] = await Promise.all([myBorrows(), listBooks()])
    borrows.value = bList
    books.value = bookList
  } finally {
    loading.value = false
  }
}

async function handleReturn(row) {
  await ElMessageBox.confirm(`确定归还《${bookTitle(row.book_id)}》吗?`, '提示', { type: 'warning' })
  await myReturn(row.id)
  ElMessage.success('还书成功')
  loadData()
}

onMounted(loadData)
</script>

<template>
  <div>
    <h2>我的借阅</h2>
    <el-table :data="borrows" v-loading="loading" border stripe>
      <el-table-column label="图书" min-width="160">
        <template #default="{ row }">{{ bookTitle(row.book_id) }}</template>
      </el-table-column>
      <el-table-column prop="borrow_date" label="借书日期" width="120" />
      <el-table-column prop="due_date" label="应还日期" width="120" />
      <el-table-column prop="return_date" label="还书日期" width="120" />
      <el-table-column label="状态" width="110">
        <template #default="{ row }">
          <el-tag :type="statusInfo(row.status).type">{{ statusInfo(row.status).text }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-button v-if="row.status === 'borrowed'" size="small" type="success" @click="handleReturn(row)">还书</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
