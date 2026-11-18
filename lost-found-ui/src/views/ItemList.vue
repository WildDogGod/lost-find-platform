<template>
  <div>
    <!-- 筛选栏 -->
    <el-card class="filter">
      <el-form :inline="true" :model="query">
        <el-form-item label="类型">
          <el-radio-group v-model="query.type" @change="load(1)">
            <el-radio-button label="">全部</el-radio-button>
            <el-radio-button label="LOST">寻物启事</el-radio-button>
            <el-radio-button label="FOUND">招领启事</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="query.categoryId" placeholder="全部分类" clearable
                     style="width: 150px" @change="load(1)">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="地点">
          <el-input v-model="query.location" placeholder="按地点筛选" clearable
                    style="width: 150px" @change="load(1)" />
        </el-form-item>
        <el-form-item label="关键词">
          <el-input v-model="query.keyword" placeholder="搜索标题/描述" clearable
                    style="width: 200px" @keyup.enter="load(1)" @clear="load(1)" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="load(1)">
            <el-icon><Search /></el-icon>搜索
          </el-button>
          <el-button @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 物品网格 -->
    <el-row :gutter="16" v-loading="loading">
      <el-col :span="6" v-for="item in items" :key="item.id" class="item-col">
        <ItemCard :item="item" />
      </el-col>
    </el-row>
    <el-empty v-if="!loading && items.length === 0" description="没有符合条件的物品" />

    <!-- 分页 -->
    <el-pagination
      v-if="total > 0"
      class="pager"
      background
      layout="total, prev, pager, next"
      :total="total"
      :page-size="query.size"
      :current-page="query.current"
      @current-change="load"
    />
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import ItemCard from '@/components/ItemCard.vue'
import { getItems } from '@/api/item'
import { getCategories } from '@/api/category'

const route = useRoute()
const categories = ref([])
const items = ref([])
const total = ref(0)
const loading = ref(false)

const query = reactive({
  current: 1,
  size: 12,
  type: route.query.type || '',
  categoryId: null,
  keyword: '',
  location: '',
  status: 'ACTIVE'
})

// 按当前筛选条件分页加载物品列表
async function load(page) {
  if (page) query.current = page
  loading.value = true
  try {
    const res = await getItems({
      current: query.current,
      size: query.size,
      type: query.type || undefined,
      categoryId: query.categoryId || undefined,
      keyword: query.keyword || undefined,
      location: query.location || undefined,
      status: 'ACTIVE'
    })
    items.value = res.records
    total.value = res.total
  } finally {
    loading.value = false
  }
}

// 清空筛选条件并回到第一页
function reset() {
  query.type = ''
  query.categoryId = null
  query.keyword = ''
  query.location = ''
  load(1)
}

onMounted(async () => {
  categories.value = await getCategories()
  load(1)
})
</script>

<style scoped>
.filter {
  margin-bottom: 20px;
  border-radius: 8px;
}

.filter :deep(.el-form-item) {
  margin-bottom: 0;
}

.item-col {
  margin-bottom: 16px;
}

.pager {
  margin-top: 20px;
  justify-content: center;
}
</style>
