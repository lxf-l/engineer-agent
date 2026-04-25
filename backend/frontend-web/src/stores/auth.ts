import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import * as authApi from '@/api/auth'
import { saveToken, removeToken, saveUserInfo, getUserInfo, clearUserInfo, getToken } from '@/utils/storage'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(getUserInfo())
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isRefreshing = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)

  // Actions
  async function login(credentials: { username: string; password: string }) {
    try {
      const response = await authApi.login(credentials)
      
      accessToken.value = response.access_token
      refreshToken.value = response.refresh_token
      user.value = response.user
      
      // 持久化存储
      saveToken(response.access_token, response.refresh_token)
      saveUserInfo(response.user)
      
      return response
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  async function register(userInfo: { username: string; email: string; password: string; confirm_password: string }) {
    try {
      await authApi.register(userInfo)
    } catch (error) {
      console.error('Register failed:', error)
      throw error
    }
  }

  async function refreshAccessToken() {
    if (!refreshToken.value) {
      throw new Error('No refresh token available')
    }

    try {
      const response = await authApi.refreshToken(refreshToken.value)
      
      accessToken.value = response.access_token
      refreshToken.value = response.refresh_token
      user.value = response.user
      
      saveToken(response.access_token, response.refresh_token)
      saveUserInfo(response.user)
      
      return response
    } catch (error) {
      console.error('Token refresh failed:', error)
      throw error
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } catch (error) {
      console.error('Logout API call failed:', error)
    } finally {
      // 清除本地状态
      accessToken.value = null
      refreshToken.value = null
      user.value = null
      
      // 清除持久化存储
      removeToken()
      clearUserInfo()
    }
  }

  // 初始化时从存储恢复登录状态
  function initAuth() {
    const token = getToken()
    const userInfo = getUserInfo()
    
    if (token && userInfo) {
      accessToken.value = token
      user.value = userInfo
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isRefreshing,
    isAuthenticated,
    login,
    register,
    refreshAccessToken,
    logout,
    initAuth,
  }
})
