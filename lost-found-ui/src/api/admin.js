import request from './request'

// 管理员分页查询物品（含待审核）
export function getAdminItems(params) {
  return request({ url: '/admin/items', method: 'get', params })
}

// 审核物品
export function auditItem(id, data) {
  return request({ url: `/admin/items/${id}/audit`, method: 'put', data })
}

// 管理员分页查询用户
export function getAdminUsers(params) {
  return request({ url: '/admin/users', method: 'get', params })
}

// 封禁/解封用户
export function updateUserStatus(id, status) {
  return request({ url: `/admin/users/${id}/status`, method: 'put', data: { status } })
}

// 数据统计
export function getStats() {
  return request({ url: '/admin/stats', method: 'get' })
}
