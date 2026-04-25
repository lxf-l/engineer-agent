<template>
  <div class="app-layout">
    <!-- 移动端抽屉菜单 -->
    <el-drawer v-if="shouldHideSidebar" v-model="drawerVisible" direction="ltr" :size="240">
      <template #header>
        <div class="drawer-header">
          <img src="@/assets/logo.svg" alt="Logo" class="logo" />
          <span class="app-title">工程AI智能体</span>
        </div>
      </template>
      <AppSidebar :collapsed="false" @close="drawerVisible = false" />
    </el-drawer>

    <!-- 桌面端侧边栏 -->
    <div v-else class="sidebar-container" :class="{ collapsed: shouldCollapseSidebar }">
      <AppSidebar :collapsed="shouldCollapseSidebar" />
    </div>

    <!-- 主内容区 -->
    <div class="main-container">
      <!-- 顶部栏 -->
      <AppHeader @menu-toggle="drawerVisible = true" />

      <!-- 内容区 -->
      <main class="content-area">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import { useResponsive } from '@/composables/useResponsive'

const { shouldCollapseSidebar, shouldHideSidebar } = useResponsive()
const drawerVisible = ref(false)
</script>

<style scoped lang="scss">
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar-container {
  width: 240px;
  transition: width 0.3s ease;

  &.collapsed {
    width: 64px;
  }
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f5f7fa;
}

.drawer-header {
  display: flex;
  align-items: center;
  gap: 12px;

  .logo {
    width: 40px;
    height: 40px;
  }

  .app-title {
    font-size: 18px;
    font-weight: bold;
    color: #303133;
  }
}

// 页面切换动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
