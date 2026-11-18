import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  // 登录成功后保存
  function setLogin(tokenValue, info) {
    token.value = tokenValue
    userInfo.value = info
    localStorage.setItem('token', tokenValue)
    localStorage.setItem('userInfo', JSON.stringify(info))
  }

  // 退出登录
  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  // 刷新缓存的用户信息（如修改资料后同步顶部头像、姓名）
  function setUserInfo(info) {
    userInfo.value = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  }

  // 是否管理员
  function isAdmin() {
    return userInfo.value && userInfo.value.role === 'ADMIN'
  }

  return { token, userInfo, setLogin, setUserInfo, logout, isAdmin }
})
