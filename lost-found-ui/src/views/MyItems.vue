<!--
  我的发布页
  管理自己发布的物品，支持编辑、关闭、查看认领申请
-->

<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <h3>我的发布</h3>
        <el-radio-group v-model="typeFilter" @change="load(1)">
          <el-radio-button label="">全部</el-radio-button>
          <el-radio-button label="LOST">寻物</el-radio-button>
          <el-radio-button label="FOUND">招领</el-radio-button>
        </el-radio-group>
      </div>
    </template>

    <el-table :data="items" v-loading="loading" border>
      <el-table-column prop="title" label="标题" min-width="160" />
      <el-table-column label="类型" width="80">
        <template #default="{ row }">
          <el-tag :type="row.type === 'LOST' ? 'danger' : 'success'" size="small">
            {{ row.type === 'LOST' ? '寻物' : '招领' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="location" label="地点" min-width="120" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusMap[row.status]?.type || 'info'" size="small">
            {{ statusMap[row.status]?.text || row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="发布时间" width="160">
        <template #default="{ row }">{{ formatTime(row.createTime) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="280" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="router.push(`/item/${row.id}`)">查看</el-button>
          <el-button link type="warning" @click="openClaims(row)">认领记录</el-button>
          <el-button v-if="row.status === 'ACTIVE' || row.status === 'PENDING'"
                     link type="info" @click="closeItem(row)">下架</el-button>
          <el-button link type="danger" @click="remove(row)">删除</el-button>
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
      :current-page="current"
      @current-change="load"
    />
  </el-card>

  <!-- 认领记录弹窗 -->
  <el-dialog v-model="claimsDialog" title="认领记录" width="640px">
    <el-table :data="claims" v-loading="claimsLoading" border>
      <el-table-column label="申请人" width="120">
        <template #default="{ row }">用户#{{ row.applicantId }}</template>
      </el-table-column>
      <el-table-column prop="claimDesc" label="特征凭证" min-width="180" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="claimStatusType(row.status)" size="small">{{ claimStatusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <template v-if="row.status === 'PENDING'">
            <el-button link type="success" @click="doReview(row, 'APPROVED')">通过</el-button>
            <el-button link type="danger" @click="doReview(row, 'REJECTED')">拒绝</el-button>
          </template>
          <span v-else class="muted">{{ row.reviewRemark || '-' }}</span>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMyItems, deleteItem, updateItemStatus } from '@/api/item'
import { getItemClaims, reviewClaim } from '@/api/claim'

const router = useRouter()
const loading = ref(false)
const items = ref([])
const typeFilter = ref('')
const current = ref(1)
const size = ref(10)
const total = ref(0)

const statusMap = {
  PENDING: { text: '待审核', type: 'info' },
  ACTIVE: { text: '进行中', type: 'success' },
  PROCESSING: { text: '认领中', type: 'warning' },
  COMPLETED: { text: '已完成', type: 'success' },
  CLOSED: { text: '已下架', type: 'info' }
}

const claimsDialog = ref(false)
const claimsLoading = ref(false)
const claims = ref([])
let currentRow = null

// 格式化发布时间
function formatTime(t) {
  return t ? String(t).replace('T', ' ').substring(0, 16) : '-'
}

// 分页加载我发布的物品
async function load(page) {
  if (page) current.value = page
  loading.value = true
  try {
    const res = await getMyItems({
      current: current.value,
      size: size.value,
      type: typeFilter.value || undefined
    })
    items.value = res.records
    total.value = res.total
  } finally {
    loading.value = false
  }
}

// 打开该物品的认领申请列表
async function openClaims(row) {
  currentRow = row
  claimsDialog.value = true
  claimsLoading.value = true
  try {
    claims.value = await getItemClaims(row.id)
  } finally {
    claimsLoading.value = false
  }
}

// 通过或驳回某条认领申请
async function doReview(row, status) {
  const reviewRemark = status === 'APPROVED' ? '审核通过' : '信息不符，予以拒绝'
  await reviewClaim(row.id, { status, reviewRemark })
  ElMessage.success(status === 'APPROVED' ? '已通过认领' : '已拒绝认领')
  claims.value = await getItemClaims(currentRow.id)
  load()
}

// 关闭（下架）该物品信息
async function closeItem(row) {
  await ElMessageBox.confirm('确定下架该信息吗？', '提示', { type: 'warning' })
  await updateItemStatus(row.id, 'CLOSED')
  ElMessage.success('已下架')
  load()
}

// 删除该物品信息
async function remove(row) {
  await ElMessageBox.confirm('确定删除该信息吗？删除后不可恢复', '提示', { type: 'warning' })
  await deleteItem(row.id)
  ElMessage.success('已删除')
  load()
}

function claimStatusType(s) {
  return s === 'APPROVED' ? 'success' : s === 'REJECTED' ? 'danger' : 'warning'
}

function claimStatusText(s) {
  return s === 'APPROVED' ? '已通过' : s === 'REJECTED' ? '已拒绝' : '待审核'
}

onMounted(() => load(1))
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  color: #303133;
}

.pager {
  margin-top: 16px;
  justify-content: center;
}

.muted {
  color: #c0c4cc;
  font-size: 12px;
}
</style>
