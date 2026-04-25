import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

// 创建Axios实例
const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    
    // 添加认证头
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`
    }
    
    // 添加请求时间戳（可选，用于调试）
    console.log(`[Request] ${config.method?.toUpperCase()} ${config.url}`, {
      params: config.params,
      data: config.data,
    })
    
    return config
  },
  (error) => {
    console.error('[Request Error]', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`[Response] ${response.config.url}`, {
      status: response.status,
      data: response.data,
    })
    
    return response.data
  },
  async (error) => {
    console.error('[Response Error]', error)
    
    const authStore = useAuthStore()
    
    // 处理401未授权错误
    if (error.response?.status === 401) {
      // 尝试刷新token
      if (!authStore.isRefreshing) {
        authStore.isRefreshing = true
        
        try {
          await authStore.refreshAccessToken()
          authStore.isRefreshing = false
          
          // 重试原请求
          return service(error.config)
        } catch (refreshError) {
          authStore.isRefreshing = false
          authStore.logout()
          ElMessage.error('登录已过期，请重新登录')
          window.location.href = '/login'
        }
      }
    }
    
    // 处理其他错误
    const message = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(message)
    
    return Promise.reject(error)
  }
)

// 导出配置函数
export function setupAxiosDefaults(config: AxiosRequestConfig) {
  Object.assign(service.defaults, config)
}

export default service
