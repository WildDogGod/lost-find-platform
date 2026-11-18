<!--
  后台信息审核页
  查看待审核物品，执行通过或驳回并填写审核备注
-->

<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <h3>物品审核</h3>
        <el-radio-group v-model="statusFilter" @change="load(1)">
          <el-radio-button label="PENDING">待审核</el-radio-button>
          <el-radio-button label="ACTIVE">已通过</el-radio-button>
          <el-radio-button label="CLOSED">已驳回</el-radio-button>
          <el-radio-button label="">全部</el-radio-button>
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
      <el-table-column label="发布者" width="100">
        <template #default="{ row }">#{{ row.userId }}</template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="时间" width="160">
        <template #default="{ row }">{{ formatTime(row.createTime) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="240" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="router.push(`/item/${row.id}`)">查看</el-button>
          <el-button v-if="row.status === 'PENDING'" link type="success" @click="pass(row)">通过</el-button>
          <el-button v-if="row.status === 'PENDING'" link type="danger" @click="rejectDialog = true; current = row">
            驳回
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

  <!-- 驳回弹窗 -->
  <el-dialog v-model="rejectDialog" title="驳回原因" width="460px">
    <el-input v-model="rejectReason" type="textarea" :rows="3" placeholder="请输入驳回原因" />
    <template #footer>
      <el-button @click="rejectDialog = false">取消</el-button>
      <el-button type="danger" @click="confirmReject">确认驳回</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getAdminItems, auditItem } from '@/api/admin'

const router = useRouter()
const loading = ref(false)
const items = ref([])
const statusFilter = ref('PENDING')
const page = ref(1)
const size = ref(10)
const total = ref(0)

const rejectDialog = ref(false)
const rejectReason = ref('')
let current = null

// 格式化发布时间
function formatTime(t) {
  return t ? String(t).replace('T', ' ').substring(0, 16) : '-'
}

// 把物品状态映射成标签颜色
function statusType(s) {
  return { ACTIVE: 'success', CLOSED: 'danger', PENDING: 'warning' }[s] || 'info'
}

// 把物品状态码翻译成中文
function statusText(s) {
  return { ACTIVE: '已通过', CLOSED: '已驳回', PENDING: '待审核', PROCESSING: '认领中', COMPLETED: '已完成' }[s] || s
}

// 分页加载待审核的物品
async function load(p) {
  if (p) page.value = p
  loading.value = true
  try {
    const res = await getAdminItems({
      current: page.value,
      size: size.value,
      status: statusFilter.value || undefined
    })
    items.value = res.records
    total.value = res.total
  } finally {
    loading.value = false
  }
}

// 审核通过，物品上架
async function pass(row) {
  await auditItem(row.id, { status: 'ACTIVE', auditRemark: '审核通过' })
  ElMessage.success('已通过')
  load()
}

// 确认驳回，并提交审核备注
async function confirmReject() {
  if (!rejectReason.value.trim()) {
    return ElMessage.warning('请填写驳回原因')
  }
  await auditItem(current.id, { status: 'CLOSED', auditRemark: rejectReason.value })
  ElMessage.success('已驳回')
  rejectDialog.value = false
  rejectReason.value = ''
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
