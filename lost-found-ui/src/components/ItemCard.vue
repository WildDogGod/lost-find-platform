<!--
  物品卡片组件
  列表页复用的单条物品展示，展示标题、分类、地点、时间与状态
-->

<template>
  <el-card class="item-card" shadow="hover" @click="goDetail">
    <div class="cover">
      <el-image v-if="cover" :src="cover" fit="cover" class="img" />
      <div v-else class="placeholder">
        <el-icon :size="40"><Picture /></el-icon>
      </div>
      <el-tag :type="item.type === 'LOST' ? 'danger' : 'success'" class="type-tag" size="small">
        {{ item.type === 'LOST' ? '寻物' : '招领' }}
      </el-tag>
    </div>

    <div class="body">
      <div class="title">{{ item.title }}</div>
      <div class="meta">
        <el-icon><Location /></el-icon>
        <span>{{ item.location }}</span>
      </div>
      <div class="meta">
        <el-icon><Clock /></el-icon>
        <span>{{ formatTime(item.eventTime) }}</span>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Picture, Location, Clock } from '@element-plus/icons-vue'

const props = defineProps({
  item: { type: Object, required: true }
})

const router = useRouter()

const cover = computed(() => {
  if (props.item.images) {
    return props.item.images.split(',')[0]
  }
  return ''
})

// 把后端时间字符串格式化为 年-月-日 时:分
function formatTime(t) {
  if (!t) return '未知'
  return String(t).replace('T', ' ').substring(0, 16)
}

// 跳转到该物品的详情页
function goDetail() {
  router.push(`/item/${props.item.id}`)
}
</script>

<style scoped>
.item-card {
  cursor: pointer;
  border-radius: 8px;
}

.cover {
  position: relative;
  height: 160px;
  border-radius: 6px;
  overflow: hidden;
}

.img {
  width: 100%;
  height: 100%;
}

.placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f2f5;
  color: #c0c4cc;
}

.type-tag {
  position: absolute;
  top: 8px;
  left: 8px;
}

.body {
  padding-top: 10px;
}

.title {
  font-size: 15px;
  font-weight: bold;
  color: #303133;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 8px;
}

.meta {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}
</style>
