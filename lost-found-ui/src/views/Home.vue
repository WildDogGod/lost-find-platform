<template>
  <div>
    <!-- 欢迎横幅 -->
    <div class="banner">
      <div class="banner-text">
        <h1>让每一件遗失物品回家</h1>
        <p>发布失物 / 招领信息，智能匹配，快速找回</p>
        <el-button type="primary" size="large" round @click="router.push('/publish')">
          <el-icon><Plus /></el-icon>立即发布
        </el-button>
      </div>
    </div>

    <!-- 快捷入口 -->
    <el-row :gutter="16" class="quick">
      <el-col :span="8">
        <el-card shadow="hover" class="quick-card lost" @click="goList('LOST')">
          <el-icon :size="32"><Search /></el-icon>
          <div class="quick-text">
            <h3>我丢了东西</h3>
            <p>查看招领信息</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="quick-card found" @click="goList('FOUND')">
          <el-icon :size="32"><Present /></el-icon>
          <div class="quick-text">
            <h3>我捡到东西</h3>
            <p>发布招领信息</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="quick-card all" @click="goList('')">
          <el-icon :size="32"><Grid /></el-icon>
          <div class="quick-text">
            <h3>物品大厅</h3>
            <p>浏览全部信息</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最新发布 -->
    <div class="section-header">
      <h2>最新发布</h2>
      <el-link type="primary" @click="router.push('/items')">查看更多 ></el-link>
    </div>

    <el-row :gutter="16" v-loading="loading">
      <el-col :span="6" v-for="item in items" :key="item.id" class="item-col">
        <ItemCard :item="item" />
      </el-col>
    </el-row>

    <el-empty v-if="!loading && items.length === 0" description="暂无信息，去发布第一条吧" />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Search, Present, Grid } from '@element-plus/icons-vue'
import ItemCard from '@/components/ItemCard.vue'
import { getItems } from '@/api/item'

const router = useRouter()
const items = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await getItems({ current: 1, size: 8, status: 'ACTIVE' })
    items.value = res.records
  } finally {
    loading.value = false
  }
})

// 按类型（寻物 / 招领）跳转到列表页
function goList(type) {
  router.push({ path: '/items', query: type ? { type } : {} })
}
</script>

<style scoped>
.banner {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  border-radius: 12px;
  padding: 48px 40px;
  color: #fff;
  margin-bottom: 20px;
}

.banner-text h1 {
  font-size: 30px;
  margin-bottom: 12px;
}

.banner-text p {
  font-size: 16px;
  margin-bottom: 24px;
  opacity: 0.95;
}

.quick {
  margin-bottom: 24px;
}

.quick-card {
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
}

.quick-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  gap: 14px;
  width: 100%;
}

.quick-card.lost .el-icon { color: #f56c6c; }
.quick-card.found .el-icon { color: #67c23a; }
.quick-card.all .el-icon { color: #409eff; }

.quick-text h3 {
  font-size: 16px;
  color: #303133;
}

.quick-text p {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h2 {
  font-size: 20px;
  color: #303133;
}

.item-col {
  margin-bottom: 16px;
}
</style>
