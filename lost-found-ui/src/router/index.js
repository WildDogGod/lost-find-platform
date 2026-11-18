/**
 * 前端路由表
 * 定义前台页面与后台管理路由，包含登录校验与管理员守卫
 */

import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/layout/Layout.vue'
import AdminLayout from '@/layout/AdminLayout.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册' }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [
      { path: 'home', name: 'Home', component: () => import('@/views/Home.vue'), meta: { title: '首页' } },
      { path: 'items', name: 'ItemList', component: () => import('@/views/ItemList.vue'), meta: { title: '物品大厅' } },
      { path: 'item/:id', name: 'ItemDetail', component: () => import('@/views/ItemDetail.vue'), meta: { title: '物品详情' } },
      { path: 'publish', name: 'ItemPublish', component: () => import('@/views/ItemPublish.vue'), meta: { title: '发布信息' } },
      { path: 'my-items', name: 'MyItems', component: () => import('@/views/MyItems.vue'), meta: { title: '我的发布' } },
      { path: 'my-claims', name: 'MyClaims', component: () => import('@/views/MyClaims.vue'), meta: { title: '我的认领' } },
      { path: 'favorites', name: 'Favorites', component: () => import('@/views/Favorites.vue'), meta: { title: '我的收藏' } },
      { path: 'messages', name: 'Messages', component: () => import('@/views/Messages.vue'), meta: { title: '消息中心' } },
      { path: 'profile', name: 'Profile', component: () => import('@/views/Profile.vue'), meta: { title: '个人信息' } }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    redirect: '/admin/audit',
    children: [
      { path: 'audit', name: 'AdminAudit', component: () => import('@/views/admin/Audit.vue'), meta: { title: '物品审核', admin: true } },
      { path: 'users', name: 'AdminUsers', component: () => import('@/views/admin/Users.vue'), meta: { title: '用户管理', admin: true } },
      { path: 'stats', name: 'AdminStats', component: () => import('@/views/admin/Stats.vue'), meta: { title: '数据统计', admin: true } }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - 校园失物招领` : '校园失物招领平台'
  const token = localStorage.getItem('token')
  if (to.path === '/login' || to.path === '/register') {
    return next()
  }
  if (!token) {
    return next('/login')
  }

  const info = JSON.parse(localStorage.getItem('userInfo') || 'null')
  const isAdmin = info && info.role === 'ADMIN'

  // 管理员登录后只能进入后台，访问前台页面一律跳转到后台
  if (isAdmin && !to.path.startsWith('/admin')) {
    return next('/admin/audit')
  }
  // 普通用户不能进入后台
  if (!isAdmin && to.path.startsWith('/admin')) {
    return next('/home')
  }
  next()
})

export default router
