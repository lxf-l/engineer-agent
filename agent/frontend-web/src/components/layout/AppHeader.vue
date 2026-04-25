<template>
  <header class="app-header">
    <div class="header-left">
      <!-- 移动端菜单按钮 -->
      <el-button v-if="isMobile" text @click="$emit('menu-toggle')">
        <el-icon :size="20"><Expand /></el-icon>
      </el-button>

      <!-- 页面标题 -->
      <h2 class="page-title">{{ pageTitle }}</h2>
    </div>

    <div class="header-right">
      <!-- 用户信息 -->
      <el-dropdown trigger="click">
        <div class="user-info">
          <el-avatar :size="32" :src="userAvatar">
            {{ username?.charAt(0)?.toUpperCase() }}
          </el-avatar>
          <span class="username">{{ username }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item disabled>
              <el-icon><User /></el-icon>
              {{ userEmail }}
            </el-dropdown-item>
            <el-dropdown-item divided @click="handleLogout">
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useResponsive } from '@/composables/useResponsive'
import { Expand, User, SwitchButton } from '@element-plus/icons-vue'
import { useAuth } from '@/composables/useAuth'

const { isMobile } = useResponsive()
const { handleLogout } = useAuth()
const route = useRoute()

const authStore = useAuthStore()
const username = computed(() => authStore.user?.username || 'User')
const userEmail = computed(() => authStore.user?.email || '')
const userAvatar = computed(() => '')
const pageTitle = computed(() => route.meta.title as string || '首页')

defineEmits<{
  'menu-toggle': []
}>()
</script>

<style scoped lang="scss">
.app-header {
  height: 60px;
  padding: 0 20px;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;

  .page-title {
    margin: 0;
    font-size: 18px;
    font-weight: 500;
    color: #303133;
  }
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;

  &:hover {
    background-color: #f5f7fa;
  }

  .username {
    font-size: 14px;
    color: #303133;
  }
}
</style>
