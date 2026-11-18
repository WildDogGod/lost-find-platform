<!--
  我的认领页
  查看自己提交的认领申请及审核结果
-->

<template>
  <el-card>
    <template #header><h3>我的认领申请</h3></template>

    <el-table :data="records" v-loading="loading" border>
      <el-table-column label="物品" min-width="160">
        <template #default="{ row }">
          <el-link type="primary" @click="router.push(`/item/${row.itemId}`)">
            查看物品 #{{ row.itemId }}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column prop="claimDesc" label="我提供的特征凭证" min-width="200" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="reviewRemark" label="审核备注" min-width="140" />
      <el-table-column label="申请时间" width="160">
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
    <el-empty v-if="!loading && records.length === 0" description="还没有认领记录" />
  </el-card>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getMyClaims } from '@/api/claim'

const router = useRouter()
const loading = ref(false)
const records = ref([])
const current = ref(1)
const size = ref(10)
const total = ref(0)

// 格式化申请时间
function formatTime(t) {
  return t ? String(t).replace('T', ' ').substring(0, 16) : '-'
}

// 认领状态映射成标签颜色
function statusType(s) {
  return s === 'APPROVED' ? 'success' : s === 'REJECTED' ? 'danger' : 'warning'
}

// 认领状态码翻译成中文
function statusText(s) {
  return s === 'APPROVED' ? '已通过' : s === 'REJECTED' ? '已拒绝' : '待审核'
}

// 分页加载我的认领记录
async function load(page) {
  if (page) current.value = page
  loading.value = true
  try {
    const res = await getMyClaims({ current: current.value, size: size.value })
    records.value = res.records
    total.value = res.total
  } finally {
    loading.value = false
  }
}

onMounted(() => load(1))
</script>

<style scoped>
.pager {
  margin-top: 16px;
  justify-content: center;
}
h3 {
  color: #303133;
}
</style>
