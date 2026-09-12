<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listReaders, searchReaders, createReader, updateReader, deleteReader } from '../api/readers'

const readers = ref([])           // 表格数据
const loading = ref(false)        // 加载开关
const keyword = ref('')           // 搜索框里的关键字
const dialogVisible = ref(false)  // 弹窗开关
const dialogTitle = ref('')       // 弹窗标题
const editingId = ref(null)       // 正在编辑的 id,null 表示新增
const form = ref({})              // 表单数据

function resetForm() {
  form.value = {
    name: '',
    phone: '',
    email: '',
    reg_date: null,
    status: 1,
  }
}

async function loadReaders() {
  loading.value = true
  try {
    readers.value = await listReaders()
  } finally {
    loading.value = false
  }
}

// 搜索:有关键字就搜索,没有就查全部
async function handleSearch() {
  loading.value = true
  try {
    readers.value = keyword.value ? await searchReaders(keyword.value) : await listReaders()
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  dialogTitle.value = '新增读者'
  resetForm()
  dialogVisible.value = true
}

function openEdit(row) {
  editingId.value = row.id
  dialogTitle.value = '编辑读者'
  form.value = {
    name: row.name,
    phone: row.phone,
    email: row.email || '',
    reg_date: row.reg_date,
    status: row.status,
  }
  dialogVisible.value = true
}

async function handleSubmit() {
  if (editingId.value === null) {
    await createReader(form.value)
    ElMessage.success('新增成功')
  } else {
    await updateReader(editingId.value, form.value)
    ElMessage.success('修改成功')
  }
  dialogVisible.value = false
  loadReaders()
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除读者「${row.name}」吗?`, '提示', { type: 'warning' })
  await deleteReader(row.id)
  ElMessage.success('删除成功')
  loadReaders()
}

onMounted(loadReaders)
</script>

<template>
  <div>
    <div class="toolbar">
      <h2>读者管理</h2>
      <div class="actions">
        <el-input
          v-model="keyword"
          placeholder="输入姓名或电话搜索"
          style="width: 220px"
          clearable
          @keyup.enter="handleSearch"
        />
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button type="success" @click="openCreate">新增读者</el-button>
      </div>
    </div>

    <el-table :data="readers" v-loading="loading" border stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="姓名" min-width="120" />
      <el-table-column prop="phone" label="电话" width="150" />
      <el-table-column prop="email" label="邮箱" min-width="180" />
      <el-table-column prop="reg_date" label="注册日期" width="130" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'info'">
            {{ row.status === 1 ? '正常' : '停用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="注册日期">
          <el-date-picker v-model="form.reg_date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="正常" :value="1" />
            <el-option label="停用" :value="0" />
          </el-select>
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
.actions {
  display: flex;
  gap: 8px;
}
</style>
