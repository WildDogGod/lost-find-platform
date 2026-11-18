import request from './request'

// 提交认领申请
export function applyClaim(data) {
  return request({ url: '/claims', method: 'post', data })
}

// 某物品的认领记录列表
export function getItemClaims(itemId) {
  return request({ url: `/claims/item/${itemId}`, method: 'get' })
}

// 我的认领记录
export function getMyClaims(params) {
  return request({ url: '/claims/mine', method: 'get', params })
}

// 审核认领申请
export function reviewClaim(id, data) {
  return request({ url: `/claims/${id}/review`, method: 'put', data })
}
