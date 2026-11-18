import request from './request'

// 发送留言
export function sendMessage(data) {
  return request({ url: '/messages', method: 'post', data })
}

// 消息列表
export function getMessages(params) {
  return request({ url: '/messages', method: 'get', params })
}

// 标记单条已读
export function readMessage(id) {
  return request({ url: `/messages/${id}/read`, method: 'put' })
}

// 全部已读
export function readAllMessages() {
  return request({ url: '/messages/read-all', method: 'put' })
}

// 未读消息数
export function getUnreadCount() {
  return request({ url: '/messages/unread-count', method: 'get' })
}
