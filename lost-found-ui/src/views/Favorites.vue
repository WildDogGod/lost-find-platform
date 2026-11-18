<!--
  我的收藏页
  展示当前用户收藏的物品，支持取消收藏与跳转详情
-->

<template>
  <el-card>
    <template #header><h3>我的收藏</h3></template>

    <el-row :gutter="16" v-loading="loading">
      <el-col :span="6" v-for="item in items" :key="item.id" class="item-col">
        <ItemCard :item="item" />
      </el-col>
    </el-row>
    <el-empty v-if="!loading && items.length === 0" description="还没有收藏任何物品" />

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
</template>

<script setup>
import { onMounted, ref } from 'vue'
import ItemCard from '@/components/ItemCard.vue'
import { getFavorites } from '@/api/favorite'
import { getItem } from '@/api/item'

const loading = ref(false)
const items = ref([])
const current = ref(1)
const size = ref(10)
const total = ref(0)

// 分页加载当前用户的收藏列表
async function load(page) {
  if (page) current.value = page
  loading.value = true
  try {
    const res = await getFavorites({ current: current.value, size: size.value })
    total.value = res.total
    // 根据收藏记录中的 itemId 拉取物品详情
    const details = await Promise.all(
      res.records.map((f) => getItem(f.itemId).catch(() => null))
    )
    items.value = details.filter(Boolean)
  } finally {
    loading.value = false
  }
}

onMounted(() => load(1))
</script>

<style scoped>
.item-col {
  margin-bottom: 16px;
}
.pager {
  margin-top: 16px;
  justify-content: center;
}
h3 {
  color: #303133;
}
</style>
