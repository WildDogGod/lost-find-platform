import request from './request'

// 当前登录用户资料
export function getProfile() {
  return request({ url: '/users/me', method: 'get' })
}

// 修改资料（只提交可编辑字段）
export function updateProfile(data) {
  return request({ url: '/users/me', method: 'put', data })
}

// 修改密码
export function updatePassword(data) {
  return request({ url: '/users/password', method: 'put', data })
}

// 学生认证
export function verifyStudent(data) {
  return request({ url: '/users/verify', method: 'post', data })
}
