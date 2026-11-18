<template>
  <div v-loading="loading">
    <el-page-header content="返回" @back="router.back()" class="back" />

    <el-row :gutter="20" v-if="item">
      <!-- 左侧图片 -->
      <el-col :span="10">
        <el-card>
          <el-image
            v-if="imageList.length"
            :src="imageList[0]"
            :preview-src-list="imageList"
            fit="cover"
            class="main-img"
          />
          <div v-else class="no-img">
            <el-icon :size="50"><Picture /></el-icon>
            <p>暂无图片</p>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧信息 -->
      <el-col :span="14">
        <el-card>
          <div class="head">
            <el-tag :type="item.type === 'LOST' ? 'danger' : 'success'">
              {{ item.type === 'LOST' ? '寻物启事' : '招领启事' }}
            </el-tag>
            <el-tag :type="statusType" effect="plain">{{ statusText }}</el-tag>
          </div>
          <h2 class="title">{{ item.title }}</h2>

          <el-descriptions :column="1" border class="desc">
            <el-descriptions-item label="丢失/拾取时间">{{ formatTime(item.eventTime) }}</el-descriptions-item>
            <el-descriptions-item label="地点">{{ item.location }}</el-descriptions-item>
            <el-descriptions-item label="联系人">{{ item.contactName }}</el-descriptions-item>
            <el-descriptions-item label="联系电话">{{ item.contactPhone }}</el-descriptions-item>
            <el-descriptions-item label="发布时间">{{ formatTime(item.createTime) }}</el-descriptions-item>
          </el-descriptions>

          <h4 class="sub-title">详细描述</h4>
          <p class="content">{{ item.description }}</p>

          <div class="actions">
            <el-button :type="favorited ? 'warning' : 'default'" @click="onFavorite">
              <el-icon><Star :filled="favorited" /></el-icon>
              {{ favorited ? '已收藏' : '收藏' }}
            </el-button>

            <el-button v-if="item.type === 'FOUND' && !isOwner && item.status === 'ACTIVE'"
                       type="primary" @click="claimDialog = true">
              <el-icon><CircleCheck /></el-icon>我要认领
            </el-button>

            <el-button v-if="!isOwner" @click="messageDialog = true">
              <el-icon><ChatDotRound /></el-icon>联系发布者
            </el-button>

            <el-button v-if="isOwner" type="success" @click="router.push('/my-items')">
              <el-icon><Tickets /></el-icon>查看认领记录
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 智能匹配 -->
    <el-card v-if="matches.length" class="matches">
      <template #header>
        <el-icon><MagicStick /></el-icon>
        智能匹配：{{ item?.type === 'LOST' ? '相关招领信息' : '相关寻物信息' }}
      </template>
      <el-row :gutter="16">
        <el-col :span="6" v-for="m in matches" :key="m.id">
          <ItemCard :item="m" />
        </el-col>
      </el-row>
    </el-card>

    <!-- 认领弹窗 -->
    <el-dialog v-model="claimDialog" title="提交认领申请" width="500px">
      <el-alert type="info" :closable="false" class="claim-tip"
                title="请详细描述物品的独有特征（如特殊标记、内部物品等），以便发布者核实" />
      <el-input v-model="claimDesc" type="textarea" :rows="4" placeholder="请描述物品特征凭证" />
      <template #footer>
        <el-button @click="claimDialog = false">取消</el-button>
        <el-button type="primary" @click="submitClaim">提交申请</el-button>
      </template>
    </el-dialog>

    <!-- 联系弹窗 -->
    <el-dialog v-model="messageDialog" title="联系发布者" width="500px">
      <el-input v-model="messageContent" type="textarea" :rows="4" placeholder="请输入留言内容" />
      <template #footer>
        <el-button @click="messageDialog = false">取消</el-button>
        <el-button type="primary" @click="submitMessage">发送</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Picture, Star, CircleCheck, ChatDotRound, Tickets, MagicStick } from '@element-plus/icons-vue'
import ItemCard from '@/components/ItemCard.vue'
import { getItem, getMatches } from '@/api/item'
import { toggleFavorite, getFavoriteStatus } from '@/api/favorite'
import { applyClaim } from '@/api/claim'
import { sendMessage } from '@/api/message'
import { useUserStore } from '@/store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const item = ref(null)
const matches = ref([])
const favorited = ref(false)
const claimDialog = ref(false)
const claimDesc = ref('')
const messageDialog = ref(false)
const messageContent = ref('')

const imageList = computed(() =>
  item.value && item.value.images ? item.value.images.split(',') : [])

const isOwner = computed(() =>
  item.value && userStore.userInfo && item.value.userId === userStore.userInfo.id)

const statusMap = {
  PENDING: { text: '待审核', type: 'info' },
  ACTIVE: { text: '进行中', type: 'success' },
  PROCESSING: { text: '认领中', type: 'warning' },
  COMPLETED: { text: '已完成', type: 'success' },
  CLOSED: { text: '已关闭', type: 'info' }
}
const statusText = computed(() => statusMap[item.value?.status]?.text || item.value?.status)
const statusType = computed(() => statusMap[item.value?.status]?.type || 'info')

// 格式化时间显示
function formatTime(t) {
  return t ? String(t).replace('T', ' ').substring(0, 16) : '-'
}

// 收藏或取消收藏，并同步按钮状态
async function onFavorite() {
  await toggleFavorite(item.value.id)
  favorited.value = !favorited.value
  ElMessage.success(favorited.value ? '已收藏' : '已取消收藏')
}

// 提交认领申请，成功后刷新物品状态
async function submitClaim() {
  if (!claimDesc.value.trim()) {
    return ElMessage.warning('请描述物品特征凭证')
  }
  await applyClaim({ itemId: item.value.id, claimDesc: claimDesc.value })
  ElMessage.success('认领申请已提交，请等待发布者审核')
  claimDialog.value = false
  claimDesc.value = ''
  loadAll()
}

// 给发布者发送站内留言
async function submitMessage() {
  if (!messageContent.value.trim()) {
    return ElMessage.warning('请输入留言内容')
  }
  await sendMessage({
    toUserId: item.value.userId,
    itemId: item.value.id,
    content: messageContent.value
  })
  ElMessage.success('留言已发送')
  messageDialog.value = false
  messageContent.value = ''
}

// 一次性加载详情、收藏状态与认领状态
async function loadAll() {
  loading.value = true
  try {
    item.value = await getItem(route.params.id)
    const [m, fav] = await Promise.all([getMatches(route.params.id), getFavoriteStatus(route.params.id)])
    matches.value = m
    favorited.value = fav.favorited
  } finally {
    loading.value = false
  }
}

onMounted(loadAll)
</script>

<style scoped>
.back {
  margin-bottom: 16px;
}

.main-img {
  width: 100%;
  height: 360px;
  border-radius: 6px;
}

.no-img {
  height: 360px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #c0c4cc;
  gap: 10px;
}

.head {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.title {
  font-size: 22px;
  color: #303133;
  margin-bottom: 18px;
}

.desc {
  margin-bottom: 18px;
}

.sub-title {
  margin: 16px 0 10px;
  color: #303133;
}

.content {
  color: #606266;
  line-height: 1.8;
  white-space: pre-wrap;
}

.actions {
  margin-top: 24px;
}

.matches {
  margin-top: 20px;
}

.claim-tip {
  margin-bottom: 14px;
}
</style>
