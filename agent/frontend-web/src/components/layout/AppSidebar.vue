<template>
  <div class="app-sidebar">
    <!-- Logo区域 -->
    <div v-if="!collapsed" class="sidebar-header">
      <img src="@/assets/logo.svg" alt="Logo" class="logo" />
      <span class="app-title">工程AI智能体</span>
    </div>
    <div v-else class="sidebar-header-collapsed">
      <img src="@/assets/logo.svg" alt="Logo" class="logo-small" />
    </div>

    <!-- 导航菜单 -->
    <el-menu
      :default-active="activeMenu"
      :collapse="collapsed"
      router
      class="sidebar-menu"
    >
      <el-menu-item index="/">
        <el-icon><HomeFilled /></el-icon>
        <template #title>首页</template>
      </el-menu-item>

      <el-menu-item index="/upload">
        <el-icon><Upload /></el-icon>
        <template #title>文档上传</template>
      </el-menu-item>

      <el-menu-item index="/files">
        <el-icon><Folder /></el-icon>
        <template #title>文件管理</template>
      </el-menu-item>

      <el-menu-item index="/query">
        <el-icon><ChatDotRound /></el-icon>
        <template #title>智能问答</template>
      </el-menu-item>

      <el-menu-item index="/report">
        <el-icon><Document /></el-icon>
        <template #title>报告生成</template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, Upload, Folder, ChatDotRound, Document } from '@element-plus/icons-vue'

const props = defineProps<{
  collapsed: boolean
}>()

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped lang="scss">
.app-sidebar {
  height: 100%;
  background-color: #304156;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  height: 60px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  background-color: #2b3a4b;

  .logo {
    width: 40px;
    height: 40px;
  }

  .app-title {
    font-size: 16px;
    font-weight: bold;
    color: #fff;
    white-space: nowrap;
  }
}

.sidebar-header-collapsed {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2b3a4b;

  .logo-small {
    width: 40px;
    height: 40px;
  }
}

.sidebar-menu {
  flex: 1;
  border-right: none;
  background-color: transparent;

  :deep(.el-menu-item) {
    color: #bfcbd9;

    &:hover {
      background-color: #263445;
      color: #fff;
    }

    &.is-active {
      background-color: #409eff;
      color: #fff;
    }

    .el-icon {
      color: inherit;
    }
  }
}
</style>
