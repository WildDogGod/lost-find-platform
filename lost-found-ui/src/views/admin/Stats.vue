<template>
  <div v-loading="loading" class="stats-page">
    <!-- 页头 -->
    <div class="page-head">
      <div>
        <h2>数据总览</h2>
        <p class="subtitle">平台运营关键指标一览</p>
      </div>
      <div class="head-actions">
        <span v-if="updatedAt" class="updated">更新于 {{ updatedAt }}</span>
        <el-button :icon="Refresh" :loading="loading" @click="load">刷新数据</el-button>
      </div>
    </div>

    <!-- 核心指标 -->
    <div class="kpi-grid">
      <div v-for="card in cards" :key="card.label" class="kpi-card" :class="card.tone">
        <div class="kpi-top">
          <span class="kpi-icon">
            <el-icon :size="20"><component :is="card.icon" /></el-icon>
          </span>
          <span class="kpi-label">{{ card.label }}</span>
        </div>
        <div class="kpi-value">{{ card.value }}</div>
        <div class="kpi-foot">{{ card.foot }}</div>
      </div>
    </div>

    <!-- 构成 + 完成情况 -->
    <div class="mid-grid">
      <el-card shadow="never" class="panel">
        <template #header>
          <div class="panel-head">
            <div class="panel-title">
              <el-icon><PieChart /></el-icon>
              <span>信息构成</span>
            </div>
            <span class="panel-hint">寻物 vs 招领</span>
          </div>
        </template>

        <div class="donut-wrap">
          <div class="donut" :style="donutStyle">
            <div class="donut-inner">
              <span class="donut-total">{{ fmt(stats?.totalItems) }}</span>
              <span class="donut-caption">总信息</span>
            </div>
          </div>

          <div class="legend">
            <div class="legend-item">
              <span class="dot lost"></span>
              <div class="legend-text">
                <span class="legend-name">寻物启事</span>
                <span class="legend-sub">占比 {{ lostShare }}%</span>
              </div>
              <strong class="legend-value">{{ fmt(stats?.lostCount) }}</strong>
            </div>
            <div class="legend-item">
              <span class="dot found"></span>
              <div class="legend-text">
                <span class="legend-name">招领启事</span>
                <span class="legend-sub">占比 {{ foundShare }}%</span>
              </div>
              <strong class="legend-value">{{ fmt(stats?.foundCount) }}</strong>
            </div>
          </div>
        </div>
      </el-card>

      <el-card shadow="never" class="panel">
        <template #header>
          <div class="panel-head">
            <div class="panel-title">
              <el-icon><Aim /></el-icon>
              <span>处理进度</span>
            </div>
            <span class="panel-hint">已完成 / 信息总数</span>
          </div>
        </template>

        <div class="progress-wrap">
          <el-progress
            type="circle"
            :percentage="successPercent"
            :width="146"
            :stroke-width="12"
            color="#6c5ce7"
          >
            <template #default="{ percentage }">
              <div class="ring-value">{{ percentage }}<small>%</small></div>
              <div class="ring-label">完成率</div>
            </template>
          </el-progress>

          <div class="progress-facts">
            <div class="fact">
              <span class="fact-label">已完成</span>
              <strong class="fact-value done">{{ fmt(stats?.completedCount) }}</strong>
            </div>
            <div class="fact">
              <span class="fact-label">信息总数</span>
              <strong class="fact-value">{{ fmt(stats?.totalItems) }}</strong>
            </div>
            <div class="fact">
              <span class="fact-label">未完成</span>
              <strong class="fact-value pending">{{ fmt(unfinishedCount) }}</strong>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 分类分布 -->
    <el-card shadow="never" class="panel category-panel">
      <template #header>
        <div class="panel-head">
          <div class="panel-title">
            <el-icon><Histogram /></el-icon>
            <span>物品分类分布</span>
          </div>
          <span class="panel-hint">共 {{ fmt(stats?.totalItems) }} 件物品</span>
        </div>
      </template>

      <div v-if="sortedDistribution.length" class="category-list">
        <div v-for="(item, index) in sortedDistribution" :key="item.categoryName" class="category-row">
          <span class="rank" :class="'rank-' + (index + 1)">{{ index + 1 }}</span>
          <div class="category-main">
            <div class="category-top">
              <span class="category-name">{{ item.categoryName }}</span>
              <span class="category-meta">{{ fmt(item.count) }} 件 · {{ shareOf(item.count) }}%</span>
            </div>
            <div class="track">
              <div
                class="fill"
                :style="{ width: barWidth(item.count), background: barColor(index) }"
              ></div>
            </div>
          </div>
        </div>
      </div>
      <el-empty v-else description="暂无分类数据" :image-size="90" />
    </el-card>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import {
  User, Files, Search, Bell, CircleCheck, TrendCharts,
  Refresh, PieChart, Histogram, Aim
} from '@element-plus/icons-vue'
import { getStats } from '@/api/admin'

const loading = ref(false)
const stats = ref(null)
const updatedAt = ref('')

const numberFormat = new Intl.NumberFormat('zh-CN')

// 数字格式化，大数字加千分位
function fmt(value) {
  if (value === null || value === undefined) return '—'
  return numberFormat.format(Number(value) || 0)
}

const totalItems = computed(() => Number(stats.value?.totalItems) || 0)
const lostCount = computed(() => Number(stats.value?.lostCount) || 0)
const foundCount = computed(() => Number(stats.value?.foundCount) || 0)
const completedCount = computed(() => Number(stats.value?.completedCount) || 0)
const unfinishedCount = computed(() => Math.max(0, totalItems.value - completedCount.value))

const lostShare = computed(() => percent(lostCount.value, totalItems.value))
const foundShare = computed(() => percent(foundCount.value, totalItems.value))
const successPercent = computed(() =>
  Math.round(Math.min(1, Math.max(0, Number(stats.value?.successRate) || 0)) * 100))

const cards = computed(() => {
  const s = stats.value
  return [
    {
      label: '注册用户', icon: User, tone: 'tone-blue',
      value: fmt(s?.totalUsers), foot: '平台累计注册账号'
    },
    {
      label: '信息总数', icon: Files, tone: 'tone-indigo',
      value: fmt(s?.totalItems), foot: '寻物与招领信息总量'
    },
    {
      label: '寻物启事', icon: Search, tone: 'tone-red',
      value: fmt(s?.lostCount), foot: `占全部信息 ${lostShare.value}%`
    },
    {
      label: '招领启事', icon: Bell, tone: 'tone-green',
      value: fmt(s?.foundCount), foot: `占全部信息 ${foundShare.value}%`
    },
    {
      label: '已完成', icon: CircleCheck, tone: 'tone-amber',
      value: fmt(s?.completedCount), foot: '已成功结案的信息'
    },
    {
      label: '成功率', icon: TrendCharts, tone: 'tone-purple',
      value: s ? `${(Number(s.successRate || 0) * 100).toFixed(1)}%` : '—',
      foot: '已完成 / 信息总数'
    }
  ]
})

const donutStyle = computed(() => {
  if (!totalItems.value) {
    return { background: 'conic-gradient(#e8ebf2 0 100%)' }
  }
  const p = Math.min(100, Math.max(0, (lostCount.value / totalItems.value) * 100))
  return { background: `conic-gradient(#f56c6c 0 ${p}%, #22b07d ${p}% 100%)` }
})

const sortedDistribution = computed(() =>
  [...(stats.value?.categoryDistribution || [])]
    .map((item) => ({ ...item, count: Number(item.count) || 0 }))
    .sort((a, b) => b.count - a.count))

const maxCount = computed(() =>
  Math.max(1, ...sortedDistribution.value.map((item) => item.count)))

const BAR_COLORS = [
  'linear-gradient(90deg, #6a8dff, #8fb0ff)',
  'linear-gradient(90deg, #22b07d, #5fd3a6)',
  'linear-gradient(90deg, #f5a623, #ffc85c)',
  'linear-gradient(90deg, #f56c6c, #ff9a8b)',
  'linear-gradient(90deg, #8e6cf0, #b49bff)',
  'linear-gradient(90deg, #22b8cf, #66d9e8)'
]

// 计算占比并保留一位小数
function percent(count, total) {
  if (!total) return 0
  return Math.round((count / total) * 100)
}

// 计算某分类数量在总量中的占比
function shareOf(count) {
  return percent(Number(count) || 0, totalItems.value)
}

// 把占比换算成进度条宽度
function barWidth(count) {
  const value = Number(count) || 0
  if (!value) return '0%'
  return `${Math.max(3, Math.round((value / maxCount.value) * 100))}%`
}

// 按序号取分类条形颜色
function barColor(index) {
  return BAR_COLORS[index % BAR_COLORS.length]
}

// 加载后台统计数据
async function load() {
  loading.value = true
  try {
    stats.value = await getStats()
    updatedAt.value = new Date().toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    })
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.stats-page {
  max-width: 1400px;
  margin: 0 auto;
}

/* ---------- 页头 ---------- */
.page-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.page-head h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #1f2d3d;
  letter-spacing: 0.5px;
}

.subtitle {
  margin: 6px 0 0;
  font-size: 13px;
  color: #8a94a6;
}

.head-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.updated {
  font-size: 12px;
  color: #a0a8b8;
}

/* ---------- KPI 卡片 ---------- */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 16px;
}

.kpi-card {
  --tone: #5b8ff9;
  --tone-soft: #eef3ff;
  position: relative;
  overflow: hidden;
  padding: 18px 18px 16px 20px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(31, 45, 61, 0.04);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--tone);
}

.kpi-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 26px rgba(31, 45, 61, 0.1);
}

.tone-blue { --tone: #4f7cff; --tone-soft: #eef3ff; }
.tone-indigo { --tone: #6c5ce7; --tone-soft: #f0edff; }
.tone-red { --tone: #f56c6c; --tone-soft: #fef0f0; }
.tone-green { --tone: #22b07d; --tone-soft: #e9f9f2; }
.tone-amber { --tone: #f0a020; --tone-soft: #fff6e8; }
.tone-purple { --tone: #8e6cf0; --tone-soft: #f4f0ff; }

.kpi-top {
  display: flex;
  align-items: center;
  gap: 10px;
}

.kpi-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 11px;
  background: var(--tone-soft);
  color: var(--tone);
}

.kpi-label {
  font-size: 13px;
  font-weight: 500;
  color: #667085;
}

.kpi-value {
  margin-top: 14px;
  font-size: 28px;
  font-weight: 700;
  line-height: 1.1;
  color: #1f2d3d;
  font-variant-numeric: tabular-nums;
}

.kpi-foot {
  margin-top: 8px;
  font-size: 12px;
  color: #a0a8b8;
}

/* ---------- 面板 ---------- */
.mid-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 16px;
  margin-top: 16px;
}

.panel {
  border: none;
  border-radius: 14px;
  box-shadow: 0 2px 10px rgba(31, 45, 61, 0.04);
}

.panel :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f2f5;
}

.panel :deep(.el-card__body) {
  padding: 22px 20px;
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #1f2d3d;
}

.panel-title .el-icon {
  color: #6c5ce7;
}

.panel-hint {
  font-size: 12px;
  color: #a0a8b8;
}

/* ---------- 环形图 ---------- */
.donut-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 42px;
  min-height: 196px;
}

.donut {
  position: relative;
  width: 168px;
  height: 168px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: inset 0 0 0 1px rgba(31, 45, 61, 0.03);
}

.donut-inner {
  position: absolute;
  inset: 26px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 2px 10px rgba(31, 45, 61, 0.06);
}

.donut-total {
  font-size: 26px;
  font-weight: 700;
  color: #1f2d3d;
  font-variant-numeric: tabular-nums;
}

.donut-caption {
  font-size: 12px;
  color: #a0a8b8;
}

.legend {
  display: flex;
  flex-direction: column;
  gap: 18px;
  min-width: 160px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
  flex-shrink: 0;
}

.dot.lost { background: #f56c6c; }
.dot.found { background: #22b07d; }

.legend-text {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
}

.legend-name {
  font-size: 13px;
  color: #4a5568;
}

.legend-sub {
  font-size: 12px;
  color: #a0a8b8;
}

.legend-value {
  font-size: 18px;
  color: #1f2d3d;
  font-variant-numeric: tabular-nums;
}

/* ---------- 进度 ---------- */
.progress-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  min-height: 196px;
}

.progress-wrap :deep(.el-progress-circle__track) {
  stroke: #eef0f7;
}

.ring-value {
  font-size: 30px;
  font-weight: 700;
  color: #1f2d3d;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.ring-value small {
  font-size: 15px;
  margin-left: 1px;
  color: #6c5ce7;
}

.ring-label {
  margin-top: 4px;
  font-size: 12px;
  color: #a0a8b8;
}

.progress-facts {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 130px;
}

.fact {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 18px;
  padding-bottom: 12px;
  border-bottom: 1px dashed #eef0f5;
}

.fact:last-child {
  padding-bottom: 0;
  border-bottom: none;
}

.fact-label {
  font-size: 13px;
  color: #8a94a6;
}

.fact-value {
  font-size: 18px;
  font-weight: 700;
  color: #1f2d3d;
  font-variant-numeric: tabular-nums;
}

.fact-value.done { color: #22b07d; }
.fact-value.pending { color: #f0a020; }

/* ---------- 分类分布 ---------- */
.category-panel {
  margin-top: 16px;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.category-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.rank {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  flex-shrink: 0;
  border-radius: 8px;
  background: #f2f4f8;
  color: #8a94a6;
  font-size: 13px;
  font-weight: 700;
}

.rank-1 {
  background: linear-gradient(135deg, #ffd76e, #f5a623);
  color: #fff;
  box-shadow: 0 3px 8px rgba(245, 166, 35, 0.35);
}

.rank-2 {
  background: linear-gradient(135deg, #d7dee8, #a9b6c7);
  color: #fff;
}

.rank-3 {
  background: linear-gradient(135deg, #e8b98c, #c98a52);
  color: #fff;
}

.category-main {
  flex: 1;
  min-width: 0;
}

.category-top {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 7px;
}

.category-name {
  font-size: 13.5px;
  color: #4a5568;
  font-weight: 500;
}

.category-meta {
  font-size: 12px;
  color: #a0a8b8;
  font-variant-numeric: tabular-nums;
}

.track {
  height: 10px;
  border-radius: 6px;
  background: #f3f5f9;
  overflow: hidden;
}

.fill {
  height: 100%;
  border-radius: 6px;
  transform-origin: left center;
  animation: grow 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes grow {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

/* ---------- 响应式 ---------- */
@media (max-width: 1280px) {
  .kpi-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .mid-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .page-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .donut-wrap,
  .progress-wrap {
    flex-direction: column;
    gap: 24px;
  }

  .progress-facts {
    width: 100%;
  }

  .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
