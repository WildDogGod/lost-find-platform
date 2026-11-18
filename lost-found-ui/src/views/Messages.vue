<!--
  消息中心页
  查看站内消息、标记单条或全部已读、查看关联物品
-->

<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <h3>消息中心</h3>
        <el-button type="primary" plain @click="markAll">全部已读</el-button>
      </div>
    </template>

    <el-table :data="records" v-loading="loading" border @row-click="onRowClick">
      <el-table-column label="类型" width="110">
        <template #default="{ row }">
          <el-tag :type="row.type === 'SYSTEM' ? 'primary' : 'info'" size="small">
            {{ row.type === 'SYSTEM' ? '系统通知' : '用户留言' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="content" label="内容" min-width="260">
        <template #default="{ row }">
          <span :class="{ unread: row.isRead === 0 }">{{ row.content }}</span>
        </template>
      </el-table-column>
      <el-table-column label="关联物品" width="120">
        <template #default="{ row }">
          <el-link v-if="row.itemId" type="primary" @click.stop="router.push(`/item/${row.itemId}`)">
            查看 #{{ row.itemId }}
          </el-link>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.isRead === 0 ? 'danger' : 'info'" size="small" effect="plain">
            {{ row.isRead === 0 ? '未读' : '已读' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="时间" width="160">
        <template #default="{ row }">{{ formatTime(row.createTime) }}</template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > 0"
      class="pager"
      background
      layout="total, prev, pager, next"
      :total="total"
      :page-size="size"
      :current-page="current"
      @current-change="load"
    />
    <el-empty v-if="!loading && records.length === 0" description="暂无消息" />
  </el-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getMessages, readMessage, readAllMessages } from '@/api/message'

const router = useRouter()
const loading = ref(false)
const records = ref([])
const current = ref(1)
const size = ref(10)
const total = ref(0)

// 格式化消息时间
function formatTime(t) {
  return t ? String(t).replace('T', ' ').substring(0, 16) : '-'
}

// 分页加载消息列表
async function load(page) {
  if (page) current.value = page
  loading.value = true
  try {
    const res = await getMessages({ current: current.value, size: size.value })
    records.value = res.records
    total.value = res.total
  } finally {
    loading.value = false
  }
}

// 点击消息标记已读，并打开关联物品
async function onRowClick(row) {
  if (row.isRead === 0) {
    await readMessage(row.id)
    row.isRead = 1
  }
}

// 一键全部标记已读
async function markAll() {
  await readAllMessages()
  ElMessage.success('已全部标记为已读')
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
.unread {
  font-weight: bold;
  color: #303133;
}
.pager {
  margin-top: 16px;
  justify-content: center;
}
.el-table {
  cursor: pointer;
}
</style>
