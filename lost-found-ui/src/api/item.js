import request from './request'

// 分页查询物品
export function getItems(params) {
  return request({ url: '/items', method: 'get', params })
}

// 物品详情
export function getItem(id) {
  return request({ url: `/items/${id}`, method: 'get' })
}

// 发布物品
export function publishItem(data) {
  return request({ url: '/items', method: 'post', data })
}

// 修改物品
export function updateItem(id, data) {
  return request({ url: `/items/${id}`, method: 'put', data })
}

// 删除物品
export function deleteItem(id) {
  return request({ url: `/items/${id}`, method: 'delete' })
}

// 修改物品状态
export function updateItemStatus(id, status) {
  return request({ url: `/items/${id}/status`, method: 'put', data: { status } })
}

// 我发布的物品
export function getMyItems(params) {
  return request({ url: '/items/mine', method: 'get', params })
}

// 智能匹配（相反类型）
export function getMatches(id) {
  return request({ url: `/items/${id}/matches`, method: 'get' })
}
