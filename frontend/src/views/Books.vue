<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listBooks, createBook, updateBook, deleteBook } from '../api/books'

const books = ref([])            // 表格要显示的数据
const loading = ref(false)       // 加载中的开关
const dialogVisible = ref(false) // 弹窗显示/隐藏
const dialogTitle = ref('')      // 弹窗标题(新增/编辑)
const editingId = ref(null)      // 正在编辑的 id,null 表示新增
const form = ref({})             // 表单里填的数据

// 把表单恢复成空白
function resetForm() {
  form.value = {
    title: '',
    author: '',
    price: 0,
    total_stock: 0,
    available: 0,
    publish: null,
    introduction: '',
  }
}

// 从后端加载图书列表
async function loadBooks() {
  loading.value = true
  try {
    books.value = await listBooks()
  } finally {
    loading.value = false
  }
}

// 点「新增」:清空表单,打开弹窗
function openCreate() {
  editingId.value = null
  dialogTitle.value = '新增图书'
  resetForm()
  dialogVisible.value = true
}

// 点「编辑」:把这一行的数据填进表单,打开弹窗
function openEdit(row) {
  editingId.value = row.id
  dialogTitle.value = '编辑图书'
  form.value = {
    title: row.title,
    author: row.author,
    price: Number(row.price),
    total_stock: row.total_stock,
    available: row.available,
    publish: row.publish,
    introduction: row.introduction || '',
  }
  dialogVisible.value = true
}

// 点弹窗里的「确定」:新增或修改
async function handleSubmit() {
  if (editingId.value === null) {
    await createBook(form.value)
    ElMessage.success('新增成功')
  } else {
    await updateBook(editingId.value, form.value)
    ElMessage.success('修改成功')
  }
  dialogVisible.value = false
  loadBooks()
}

// 点「删除」:先确认,再删除
async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除《${row.title}》吗?`, '提示', {
    type: 'warning',
  })
  await deleteBook(row.id)
  ElMessage.success('删除成功')
  loadBooks()
}

// 页面一打开就加载数据
onMounted(loadBooks)
</script>

<template>
  <div>
    <div class="toolbar">
      <h2>图书管理</h2>
      <el-button type="primary" @click="openCreate">新增图书</el-button>
    </div>

    <!-- 图书表格 -->
    <el-table :data="books" v-loading="loading" border stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="title" label="书名" min-width="140" />
      <el-table-column prop="author" label="作者" width="120" />
      <el-table-column prop="price" label="价格" width="90" />
      <el-table-column prop="total_stock" label="总库存" width="90" />
      <el-table-column prop="available" label="可借" width="80" />
      <el-table-column prop="publish" label="出版日期" width="120" />
      <el-table-column prop="introduction" label="简介" min-width="200" show-overflow-tooltip />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="书名">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="作者">
          <el-input v-model="form.author" />
        </el-form-item>
        <el-form-item label="价格">
          <el-input-number v-model="form.price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="总库存">
          <el-input-number v-model="form.total_stock" :min="0" />
        </el-form-item>
        <el-form-item label="可借数量">
          <el-input-number v-model="form.available" :min="0" />
        </el-form-item>
        <el-form-item label="出版日期">
          <el-date-picker v-model="form.publish" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.introduction" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
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
