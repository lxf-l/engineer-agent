<template>
  <div class="home-view">
    <el-row :gutter="20">
      <!-- 欢迎卡片 -->
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card class="welcome-card">
          <h1>欢迎使用工程AI智能体</h1>
          <p>专业的建筑工程领域AI助手，为您提供智能化的文档管理、知识问答和报告生成服务</p>
        </el-card>
      </el-col>

      <!-- 功能卡片 -->
      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="feature-card" shadow="hover">
          <el-icon :size="48" color="#409eff"><Upload /></el-icon>
          <h3>文档上传</h3>
          <p>支持PDF、DOCX、TXT格式文档，自动解析和向量化</p>
          <router-link to="/upload">
            <el-button type="primary" size="small">开始使用</el-button>
          </router-link>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="feature-card" shadow="hover">
          <el-icon :size="48" color="#67c23a"><ChatDotRound /></el-icon>
          <h3>智能问答</h3>
          <p>基于RAG技术的智能问答，精准回答工程技术问题</p>
          <router-link to="/query">
            <el-button type="success" size="small">开始使用</el-button>
          </router-link>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="feature-card" shadow="hover">
          <el-icon :size="48" color="#e6a23c"><Document /></el-icon>
          <h3>报告生成</h3>
          <p>自动生成工程报告，支持多种模板和规范引用</p>
          <router-link to="/report">
            <el-button type="warning" size="small">开始使用</el-button>
          </router-link>
        </el-card>
      </el-col>

      <!-- 统计信息 -->
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card class="stats-card">
          <h3>系统状态</h3>
          <el-row :gutter="20">
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-item">
                <div class="stat-value">{{ knowledgeStore.documents.length }}</div>
                <div class="stat-label">已上传文档</div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-item">
                <div class="stat-value">{{ authStore.user?.username || 'User' }}</div>
                <div class="stat-label">当前用户</div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useKnowledgeStore } from '@/stores/knowledge'
import { Upload, ChatDotRound, Document } from '@element-plus/icons-vue'

const authStore = useAuthStore()
const knowledgeStore = useKnowledgeStore()
</script>

<style scoped lang="scss">
.home-view {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;

  h1 {
    margin: 0 0 12px;
    font-size: 28px;
  }

  p {
    margin: 0;
    font-size: 16px;
    opacity: 0.9;
  }
}

.feature-card {
  text-align: center;
  padding: 20px;
  margin-bottom: 20px;
  transition: transform 0.3s;

  &:hover {
    transform: translateY(-5px);
  }

  h3 {
    margin: 16px 0 12px;
    font-size: 18px;
    color: #303133;
  }

  p {
    margin: 0 0 16px;
    font-size: 14px;
    color: #909399;
    min-height: 40px;
  }
}

.stats-card {
  h3 {
    margin: 0 0 20px;
    font-size: 18px;
    color: #303133;
  }
}

.stat-item {
  text-align: center;
  padding: 16px;

  .stat-value {
    font-size: 32px;
    font-weight: bold;
    color: #409eff;
    margin-bottom: 8px;
  }

  .stat-label {
    font-size: 14px;
    color: #909399;
  }
}
</style>
