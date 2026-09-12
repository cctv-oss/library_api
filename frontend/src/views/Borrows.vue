<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listBorrows, borrowBook, returnBook } from '../api/borrows'
import { listBooks } from '../api/books'
import { listReaders } from '../api/readers'

const borrows = ref([])          // 借阅记录
const books = ref([])            // 图书列表(用于显示书名 + 借书下拉)
const readers = ref([])          // 读者列表(用于显示姓名 + 借书下拉)
const loading = ref(false)
const dialogVisible = ref(false)
const form = ref({ reader_id: null, book_id: null })

// 借阅记录里只有 book_id,用这个函数把 id 换成书名
function bookTitle(id) {
  const b = books.value.find((x) => x.id === id)
  return b ? b.title : `#${id}`
}

// 同理,把 reader_id 换成读者姓名
function readerName(id) {
  const r = readers.value.find((x) => x.id === id)
  return r ? r.name : `#${id}`
}

// 借阅状态 -> 显示的文字和颜色
function statusInfo(status) {
  if (status === 'borrowed') return { text: '借阅中', type: 'warning' }
  if (status === 'returned') return { text: '已归还', type: 'success' }
  if (status === 'overdue') return { text: '逾期归还', type: 'danger' }
  return { text: status, type: 'info' }
}

// 一次性加载借阅记录、图书、读者三份数据
async function loadData() {
  loading.value = true
  try {
    const [bList, bookList, readerList] = await Promise.all([
      listBorrows(),
      listBooks(),
      listReaders(),
    ])
    borrows.value = bList
    books.value = bookList
    readers.value = readerList
  } finally {
    loading.value = false
  }
}

function openBorrow() {
  form.value = { reader_id: null, book_id: null }
  dialogVisible.value = true
}

async function handleBorrow() {
  await borrowBook(form.value.book_id, form.value.reader_id)
  ElMessage.success('借书成功')
  dialogVisible.value = false
  loadData()
}

async function handleReturn(row) {
  await ElMessageBox.confirm(`确定归还《${bookTitle(row.book_id)}》吗?`, '提示', { type: 'warning' })
  await returnBook(row.id)
  ElMessage.success('还书成功')
  loadData()
}

onMounted(loadData)
</script>

<template>
  <div>
    <div class="toolbar">
      <h2>借阅管理</h2>
      <el-button type="primary" @click="openBorrow">借书</el-button>
    </div>

    <el-table :data="borrows" v-loading="loading" border stripe>
      <el-table-column prop="id" label="记录ID" width="80" />
      <el-table-column label="读者" min-width="120">
        <template #default="{ row }">{{ readerName(row.reader_id) }}</template>
      </el-table-column>
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
          <el-button
            v-if="row.status === 'borrowed'"
            size="small"
            type="success"
            @click="handleReturn(row)"
          >
            还书
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 借书弹窗 -->
    <el-dialog v-model="dialogVisible" title="借书" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="读者">
          <el-select v-model="form.reader_id" placeholder="请选择读者" style="width: 100%">
            <el-option
              v-for="r in readers"
              :key="r.id"
              :label="r.name"
              :value="r.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="图书">
          <el-select v-model="form.book_id" placeholder="请选择图书" style="width: 100%">
            <el-option
              v-for="b in books"
              :key="b.id"
              :label="b.title"
              :value="b.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleBorrow">确定借书</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
</style>
