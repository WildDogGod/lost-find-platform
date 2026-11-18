<template>
  <el-card v-loading="loading">
    <template #header>
      <h3>个人信息</h3>
    </template>

    <el-tabs v-model="activeTab">
      <!-- ================= 基本资料 ================= -->
      <el-tab-pane label="基本资料" name="basic">
        <div class="avatar-row">
          <el-avatar :size="72" :src="form.avatar">{{ form.username?.charAt(0) }}</el-avatar>
          <div class="avatar-side">
            <el-upload
              action="/api/files/upload"
              :headers="uploadHeaders"
              name="file"
              :show-file-list="false"
              :before-upload="beforeAvatarUpload"
              :on-success="onAvatarSuccess"
              :on-error="onAvatarError"
            >
              <el-button size="small">更换头像</el-button>
            </el-upload>
            <div class="tip">支持 jpg / png / gif / webp，不超过 2MB；上传后需点「保存修改」</div>
          </div>
        </div>

        <el-form ref="basicRef" :model="form" :rules="basicRules" label-width="90px" class="form">
          <el-form-item label="账号">
            <el-input v-model="form.username" disabled />
          </el-form-item>
          <el-form-item label="真实姓名" prop="realName">
            <el-input v-model="form.realName" maxlength="50" />
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="form.phone" maxlength="20" placeholder="选填" />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="form.email" maxlength="100" placeholder="选填" />
          </el-form-item>
          <el-form-item label="学号">
            <el-input v-model="form.studentNo" disabled placeholder="通过「学生认证」提交" />
          </el-form-item>
          <el-form-item label="学院">
            <el-input v-model="form.college" disabled placeholder="通过「学生认证」提交" />
          </el-form-item>
          <el-form-item label="认证状态">
            <el-tag v-if="form.verifyStatus === 1" type="success">已认证</el-tag>
            <el-tag v-else type="warning">未认证</el-tag>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="saving" @click="onSave">保存修改</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- ================= 学生认证 ================= -->
      <el-tab-pane label="学生认证" name="verify">
        <el-alert
          v-if="form.verifyStatus === 1"
          type="success"
          :closable="false"
          show-icon
          title="已通过学生认证"
          description="学号与学院信息已与账号绑定，如需修改请联系管理员。"
        />
        <template v-else>
          <el-alert
            class="mb"
            type="info"
            :closable="false"
            show-icon
            title="提交真实姓名、学号与学院即可完成认证"
            description="认证后更容易被其他同学信任，也方便物品归还时核验身份。"
          />
          <el-form ref="verifyRef" :model="verifyForm" :rules="verifyRules" label-width="90px" class="form">
            <el-form-item label="真实姓名" prop="realName">
              <el-input v-model="verifyForm.realName" maxlength="50" />
            </el-form-item>
            <el-form-item label="学号" prop="studentNo">
              <el-input v-model="verifyForm.studentNo" maxlength="20" />
            </el-form-item>
            <el-form-item label="学院" prop="college">
              <el-input v-model="verifyForm.college" maxlength="100" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="verifying" @click="onVerify">提交认证</el-button>
            </el-form-item>
          </el-form>
        </template>
      </el-tab-pane>

      <!-- ================= 修改密码 ================= -->
      <el-tab-pane label="修改密码" name="password">
        <el-form ref="pwdRef" :model="pwdForm" :rules="pwdRules" label-width="90px" class="form">
          <el-form-item label="原密码" prop="oldPassword">
            <el-input v-model="pwdForm.oldPassword" type="password" show-password />
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input v-model="pwdForm.newPassword" type="password" show-password />
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input v-model="pwdForm.confirmPassword" type="password" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="changing" @click="onChangePassword">确认修改</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </el-card>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getProfile, updateProfile, updatePassword, verifyStudent } from '@/api/user'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

const activeTab = ref('basic')
const loading = ref(false)
const saving = ref(false)
const verifying = ref(false)
const changing = ref(false)

const basicRef = ref()
const verifyRef = ref()
const pwdRef = ref()

const form = ref({
  id: null,
  username: '',
  realName: '',
  studentNo: '',
  college: '',
  phone: '',
  email: '',
  avatar: '',
  verifyStatus: 0,
  role: ''
})

const verifyForm = ref({ realName: '', studentNo: '', college: '' })
const pwdForm = ref({ oldPassword: '', newPassword: '', confirmPassword: '' })

const uploadHeaders = computed(() => ({ Authorization: 'Bearer ' + userStore.token }))

// 选填字段：为空时不校验格式
const optionalPhone = (rule, value, callback) => {
  if (!value) return callback()
  return /^1[3-9]\d{9}$/.test(value) ? callback() : callback(new Error('手机号格式不正确'))
}

// 邮箱选填校验：为空或格式合法即可
const optionalEmail = (rule, value, callback) => {
  if (!value) return callback()
  return /^[\w.+-]+@[\w-]+(\.[\w-]+)+$/.test(value) ? callback() : callback(new Error('邮箱格式不正确'))
}

// 校验确认密码与密码是否一致
const validateConfirm = (rule, value, callback) => {
  if (value !== pwdForm.value.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const basicRules = {
  realName: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  phone: [{ validator: optionalPhone, trigger: 'blur' }],
  email: [{ validator: optionalEmail, trigger: 'blur' }]
}

const verifyRules = {
  realName: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  studentNo: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  college: [{ required: true, message: '请输入学院', trigger: 'blur' }]
}

const pwdRules = {
  oldPassword: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度需在 6-20 位之间', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validateConfirm, trigger: 'blur' }
  ]
}

// 加载当前用户资料
async function loadProfile() {
  loading.value = true
  try {
    const info = await getProfile()
    form.value = info
    // 同步刷新顶部头像与用户名
    userStore.setUserInfo(info)
    verifyForm.value = {
      realName: info.realName || '',
      studentNo: info.studentNo || '',
      college: info.college || ''
    }
  } finally {
    loading.value = false
  }
}

onMounted(loadProfile)

// 保存个人资料
async function onSave() {
  await basicRef.value.validate()
  saving.value = true
  try {
    // 只提交允许本人修改的字段，不回传 role / verifyStatus 等
    await updateProfile({
      realName: form.value.realName,
      phone: form.value.phone,
      email: form.value.email,
      avatar: form.value.avatar
    })
    ElMessage.success('保存成功')
    await loadProfile()
  } finally {
    saving.value = false
  }
}

// 提交校园实名认证
async function onVerify() {
  await verifyRef.value.validate()
  verifying.value = true
  try {
    await verifyStudent({ ...verifyForm.value })
    ElMessage.success('认证成功')
    await loadProfile()
  } finally {
    verifying.value = false
  }
}

// 校验后修改密码
async function onChangePassword() {
  await pwdRef.value.validate()
  changing.value = true
  try {
    await updatePassword({ ...pwdForm.value })
    ElMessage.success('密码修改成功')
    pwdForm.value = { oldPassword: '', newPassword: '', confirmPassword: '' }
    pwdRef.value.clearValidate()
  } finally {
    changing.value = false
  }
}

const AVATAR_MAX_MB = 2

// 头像上传前校验格式与大小
function beforeAvatarUpload(file) {
  if (!/^image\//.test(file.type)) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (file.size / 1024 / 1024 > AVATAR_MAX_MB) {
    ElMessage.error(`图片不能超过 ${AVATAR_MAX_MB}MB`)
    return false
  }
  return true
}

// 头像上传成功，回填地址
function onAvatarSuccess(response) {
  if (response.code === 200) {
    form.value.avatar = response.data.url
    ElMessage.success('头像上传成功，记得点「保存修改」')
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

// 头像上传失败提示
function onAvatarError() {
  ElMessage.error('头像上传失败，请检查后端是否启动')
}
</script>

<style scoped>
.form {
  max-width: 520px;
}

.avatar-row {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
}

.avatar-side {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tip {
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
}

.mb {
  margin-bottom: 20px;
}
</style>
