<!--
  登录页
  账号密码登录，成功后保存 token，按角色进入前台或后台
-->

<template>
  <div class="auth">
    <el-card class="card">
      <div class="title">
        <el-icon :size="30" color="#409eff"><Compass /></el-icon>
        <h2>校园失物招领平台</h2>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" @keyup.enter="onLogin">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="请输入账号" :prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码"
                    :prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-button type="primary" size="large" class="btn" :loading="loading" @click="onLogin">
          登 录
        </el-button>
      </el-form>

      <div class="footer">
        还没有账号？<el-link type="primary" @click="router.push('/register')">立即注册</el-link>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { login } from '@/api/auth'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)
const form = ref({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

// 校验表单、调用登录接口、保存 token 并按角色跳转
async function onLogin() {
  await formRef.value.validate()
  loading.value = true
  try {
    const res = await login(form.value)
    userStore.setLogin(res.token, res.userInfo)
    ElMessage.success('登录成功')
    router.push(res.userInfo?.role === 'ADMIN' ? '/admin/audit' : '/home')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
}

.card {
  width: 420px;
  padding: 20px 20px 10px;
  border-radius: 12px;
}

.title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 28px;
}

.title h2 {
  font-size: 22px;
  color: #303133;
}

.btn {
  width: 100%;
}

.footer {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
}
</style>
