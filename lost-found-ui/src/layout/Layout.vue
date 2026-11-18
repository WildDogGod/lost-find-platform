<!--
  前台整体布局
  顶部导航、用户菜单、未读消息角标与内容区，登录后使用
-->

<template>
  <el-container class="layout">
    <el-header class="header">
      <div class="logo" @click="router.push('/home')">
        <el-icon :size="26" color="#409eff"><Compass /></el-icon>
        <span>校园失物招领</span>
      </div>

      <el-menu
        :default-active="activeMenu"
        mode="horizontal"
        :ellipsis="false"
        router
        class="menu"
      >
        <el-menu-item index="/home">首页</el-menu-item>
        <el-menu-item index="/items">物品大厅</el-menu-item>
        <el-menu-item index="/publish">发布信息</el-menu-item>
        <el-menu-item index="/my-items">我的发布</el-menu-item>
        <el-menu-item index="/my-claims">我的认领</el-menu-item>
        <el-menu-item index="/favorites">我的收藏</el-menu-item>
        <el-menu-item index="/messages">
          <el-badge :value="unread" :hidden="unread === 0" class="badge">消息中心</el-badge>
        </el-menu-item>
      </el-menu>

      <el-dropdown @command="onCommand">
        <span class="user">
          <el-avatar :size="30" :src="userInfo?.avatar">
            {{ userInfo?.username?.charAt(0) }}
          </el-avatar>
          <span class="username">{{ userInfo?.username }}</span>
          <el-icon><ArrowDown /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">个人信息</el-dropdown-item>
            <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-header>

    <el-main class="main">
      <router-view />
    </el-main>

    <el-footer class="footer">
      校园失物招领平台 · 课程设计 © 2026
    </el-footer>
  </el-container>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useUserStore } from '@/store/user'
import { getUnreadCount } from '@/api/message'
import { logout as logoutApi } from '@/api/auth'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const userInfo = computed(() => userStore.userInfo)
const activeMenu = computed(() => route.path)
const unread = ref(0)

// 拉取未读消息数量，用于导航栏红点角标
async function loadUnread() {
  try {
    const res = await getUnreadCount()
    unread.value = res.count
  } catch (e) {
    // 忽略
  }
}

let timer = null
onMounted(() => {
  loadUnread()
  timer = setInterval(loadUnread, 15000)
})
onUnmounted(() => {
  if (timer) clearInterval(timer)
})

// 处理用户菜单下拉：个人中心 / 我的发布 / 退出登录
async function onCommand(command) {
  if (command === 'logout') {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', { type: 'warning' })
    try {
      await logoutApi()
    } catch (e) {
      // 即使后端调用失败，也清理本地登录态
    }
    userStore.logout()
    router.push('/login')
  } else if (command === 'profile') {
    router.push('/profile')
  }
}
</script>

<style scoped>
.layout {
  min-height: 100%;
}

.header {
  display: flex;
  align-items: center;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 24px;
  height: 60px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  cursor: pointer;
  white-space: nowrap;
  margin-right: 30px;
}

.menu {
  flex: 1;
  border-bottom: none;
}

.badge {
  margin-top: 8px;
}

.user {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  white-space: nowrap;
}

.username {
  font-size: 14px;
  color: #303133;
}

.main {
  padding: 20px 24px;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

.footer {
  text-align: center;
  color: #909399;
  font-size: 13px;
  height: 60px;
  line-height: 60px;
}
</style>
