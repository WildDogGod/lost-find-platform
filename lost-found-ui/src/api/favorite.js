import request from './request'

// 收藏 / 取消收藏（切换）
export function toggleFavorite(itemId) {
  return request({ url: `/favorites/${itemId}/toggle`, method: 'post' })
}

// 我的收藏列表
export function getFavorites(params) {
  return request({ url: '/favorites', method: 'get', params })
}

// 查询某物品是否已收藏
export function getFavoriteStatus(itemId) {
  return request({ url: `/favorites/${itemId}/status`, method: 'get' })
}
