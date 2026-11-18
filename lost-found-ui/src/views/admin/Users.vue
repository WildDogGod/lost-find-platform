<!--
  后台用户管理页
  查看用户列表，封禁或解封账号
-->

<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <h3>用户管理</h3>
        <el-input v-model="keyword" placeholder="搜索账号/姓名/学号" clearable
                  style="width: 260px" @keyup.enter="load(1)" @clear="load(1)">
          <template #append>
            <el-button @click="load(1)"><el-icon><Search /></el-icon></el-button>
          </template>
        </el-input>
      </div>
    </template>

    <el-table :data="users" v-loading="loading" border>
      <el-table-column prop="username" label="账号" width="120" />
      <el-table-column prop="realName" label="姓名" width="100" />
      <el-table-column prop="studentNo" label="学号" width="130" />
      <el-table-column prop="college" label="学院" min-width="140" />
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column label="角色" width="90">
        <template #default="{ row }">
          <el-tag :type="row.role === 'ADMIN' ? 'danger' : 'info'" size="small">
            {{ row.role === 'ADMIN' ? '管理员' : '用户' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="认证" width="80">
        <template #default="{ row }">
          <el-tag :type="row.verifyStatus === 1 ? 'success' : 'info'" size="small" effect="plain">
            {{ row.verifyStatus === 1 ? '已认证' : '未认证' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'danger' : 'success'" size="small">
            {{ row.status === 1 ? '已封禁' : '正常' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button v-if="row.role !== 'ADMIN'" link
                     :type="row.status === 1 ? 'success' : 'danger'" @click="toggleStatus(row)">
            {{ row.status === 1 ? '解封' : '封禁' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > 0"
      class="pager"
      background
      layout="total, prev, pager, next"
      :total="total"
      :page-size="size"
      :current-page="page"
      @current-change="load"
    />
  </el-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getAdminUsers, updateUserStatus } from '@/api/admin'

const loading = ref(false)
const users = ref([])
const keyword = ref('')
const page = ref(1)
const size = ref(10)
const total = ref(0)

// 分页加载用户列表
async function load(p) {
  if (p) page.value = p
  loading.value = true
  try {
    const res = await getAdminUsers({
      current: page.value,
      size: size.value,
      keyword: keyword.value || undefined
    })
    users.value = res.records
    total.value = res.total
  } finally {
    loading.value = false
  }
}

// 封禁或解封用户账号
async function toggleStatus(row) {
  const next = row.status === 1 ? 0 : 1
  await ElMessageBox.confirm(
    next === 1 ? `确定封禁用户「${row.username}」吗？` : `确定解封「${row.username}」吗？`,
    '提示', { type: 'warning' }
  )
  await updateUserStatus(row.id, next)
  ElMessage.success(next === 1 ? '已封禁' : '已解封')
  load()
}

onMounted(() => load(1))
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
h3 {
  color: #303133;
}
.pager {
  margin-top: 16px;
  justify-content: center;
}
</style>
