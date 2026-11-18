<!--
  发布物品页
  填写失物 / 招领信息、选择分类、上传图片并提交
-->

<template>
  <el-card>
    <template #header>
      <h3>发布失物 / 招领信息</h3>
    </template>

    <el-form ref="formRef" :model="form" :rules="rules" label-width="110px" class="form">
      <el-form-item label="信息类型" prop="type">
        <el-radio-group v-model="form.type">
          <el-radio label="LOST">寻物启事（我丢了东西）</el-radio>
          <el-radio label="FOUND">招领启事（我捡到东西）</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="物品标题" prop="title">
        <el-input v-model="form.title" placeholder="如：黑色钱包 / 校园卡" maxlength="50" show-word-limit />
      </el-form-item>

      <el-form-item label="物品分类" prop="categoryId">
        <el-select v-model="form.categoryId" placeholder="请选择分类" style="width: 240px">
          <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>

      <el-form-item label="物品图片">
        <el-upload
          ref="uploadRef"
          action="/api/files/upload"
          :headers="uploadHeaders"
          list-type="picture-card"
          name="file"
          accept="image/*"
          :limit="5"
          :before-upload="beforeUpload"
          :on-success="onUploadSuccess"
          :on-error="onUploadError"
          :on-remove="onRemove"
          :on-preview="onPreview"
          :on-exceed="onExceed"
        >
          <el-icon><Plus /></el-icon>
        </el-upload>
        <div class="tip">最多上传 5 张清晰图片，单张不超过 5MB，有助于找回（可选）</div>
      </el-form-item>

      <el-form-item label="详细描述" prop="description">
        <el-input v-model="form.description" type="textarea" :rows="4"
                  placeholder="请描述物品外观、颜色、内含物品等" maxlength="500" show-word-limit />
      </el-form-item>

      <el-form-item v-if="form.type === 'FOUND'" label="隐藏特征">
        <el-input v-model="form.secretFeature" placeholder="仅你可见，用于核验冒领（如物品内部标记）" />
      </el-form-item>

      <el-form-item label="发生时间" prop="eventTime">
        <el-date-picker v-model="form.eventTime" type="datetime" placeholder="选择丢失/拾取时间"
                        value-format="YYYY-MM-DDTHH:mm:ss" style="width: 240px" />
      </el-form-item>

      <el-form-item label="地点" prop="location">
        <el-input v-model="form.location" placeholder="如：图书馆三楼 / 第二食堂" />
      </el-form-item>

      <el-form-item label="联系人" prop="contactName">
        <el-input v-model="form.contactName" style="width: 240px" />
      </el-form-item>

      <el-form-item label="联系电话" prop="contactPhone">
        <el-input v-model="form.contactPhone" style="width: 240px" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" :loading="submitting" @click="onSubmit">提交发布</el-button>
        <el-button @click="router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </el-card>

  <el-image-viewer v-if="previewVisible" :url-list="imageUrls" @close="previewVisible = false" />
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getCategories } from '@/api/category'
import { publishItem } from '@/api/item'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const uploadRef = ref()
const categories = ref([])
const submitting = ref(false)
const imageUrls = ref([])
const previewVisible = ref(false)

const form = ref({
  type: 'LOST',
  title: '',
  categoryId: null,
  description: '',
  images: '',
  secretFeature: '',
  eventTime: '',
  location: '',
  contactName: userStore.userInfo?.realName || '',
  contactPhone: userStore.userInfo?.phone || ''
})

const uploadHeaders = computed(() => ({
  Authorization: 'Bearer ' + userStore.token
}))

const rules = {
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  categoryId: [{ required: true, message: '请选择分类', trigger: 'change' }],
  description: [{ required: true, message: '请输入描述', trigger: 'blur' }],
  eventTime: [{ required: true, message: '请选择时间', trigger: 'change' }],
  location: [{ required: true, message: '请输入地点', trigger: 'blur' }],
  contactName: [{ required: true, message: '请输入联系人', trigger: 'blur' }],
  contactPhone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }]
}

// 上传前校验图片格式与大小
function beforeUpload(file) {
  if (!file.type.startsWith('image/')) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 5MB')
    return false
  }
  return true
}

// 上传成功回调，收集图片访问地址
function onUploadSuccess(response) {
  if (response.code === 200) {
    imageUrls.value.push(response.data.url)
  } else {
    ElMessage.error(response.message || '上传失败')
  }
}

// 上传失败提示
function onUploadError() {
  ElMessage.error('图片上传失败，请检查网络后重试')
}

// 超出图片数量上限的提示
function onExceed() {
  ElMessage.warning('最多上传 5 张图片')
}

// 移除已上传的图片
function onRemove(uploadFile) {
  const url = uploadFile.response?.data?.url
  imageUrls.value = imageUrls.value.filter((u) => u !== url)
}

// 预览已上传的图片
function onPreview() {
  previewVisible.value = true
}

// 校验表单并提交发布请求
async function onSubmit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    form.value.images = imageUrls.value.join(',')
    await publishItem(form.value)
    ElMessage.success('发布成功，等待管理员审核')
    router.push('/my-items')
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  categories.value = await getCategories()
})
</script>

<style scoped>
.form {
  max-width: 760px;
}

.tip {
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
}
</style>
