<!--
  注册页
  填写账号、密码与校园信息完成注册
-->

<template>
  <div class="auth">
    <el-card class="card">
      <h2 class="title">用户注册</h2>

      <el-form ref="formRef" :model="form" :rules="rules">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="账号（4-20位）" :prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码（6-20位）"
                    :prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item prop="confirm">
          <el-input v-model="form.confirm" type="password" placeholder="确认密码"
                    :prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item prop="realName">
          <el-input v-model="form.realName" placeholder="真实姓名" :prefix-icon="Postcard" />
        </el-form-item>
        <el-form-item prop="studentNo">
          <el-input v-model="form.studentNo" placeholder="学号（选填）" :prefix-icon="Reading" />
        </el-form-item>
        <el-form-item prop="phone">
          <el-input v-model="form.phone" placeholder="手机号（选填）" :prefix-icon="Phone" />
        </el-form-item>

        <el-button type="primary" class="btn" :loading="loading" @click="onRegister">
          注 册
        </el-button>
      </el-form>

      <div class="footer">
        已有账号？<el-link type="primary" @click="router.push('/login')">返回登录</el-link>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Postcard, Reading, Phone } from '@element-plus/icons-vue'
import { register } from '@/api/auth'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = ref({
  username: '',
  password: '',
  confirm: '',
  realName: '',
  studentNo: '',
  phone: ''
})

// 校验确认密码与密码是否一致
const validateConfirm = (rule, value, callback) => {
  if (value !== form.value.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    { min: 4, max: 20, message: '账号长度需在 4-20 位之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度需在 6-20 位之间', trigger: 'blur' }
  ],
  confirm: [{ required: true, validator: validateConfirm, trigger: 'blur' }],
  realName: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }]
}

// 校验表单并提交注册请求
async function onRegister() {
  await formRef.value.validate()
  loading.value = true
  try {
    await register({
      username: form.value.username,
      password: form.value.password,
      realName: form.value.realName,
      studentNo: form.value.studentNo,
      phone: form.value.phone
    })
    ElMessage.success('注册成功，请登录')
    router.push('/login')
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
  padding: 10px 20px;
  border-radius: 12px;
}

.title {
  text-align: center;
  margin-bottom: 24px;
  color: #303133;
}

.btn {
  width: 100%;
}

.footer {
  text-align: center;
  margin-top: 12px;
  font-size: 14px;
}
</style>
