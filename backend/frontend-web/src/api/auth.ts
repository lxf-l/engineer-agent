import request from './client'
import type { LoginRequest, RegisterRequest, AuthResponse, User } from '@/types'

/**
 * 用户登录
 */
export function login(data: LoginRequest): Promise<AuthResponse> {
  return request.post('/auth/login', data)
}

/**
 * 用户注册
 */
export function register(data: RegisterRequest): Promise<void> {
  return request.post('/auth/register', data)
}

/**
 * 刷新Token
 */
export function refreshToken(refreshToken: string): Promise<AuthResponse> {
  return request.post('/auth/refresh', { refresh_token: refreshToken })
}

/**
 * 获取当前用户信息
 */
export function getCurrentUser(): Promise<User> {
  // 注意：当前后端没有实现/me接口，需要后续添加
  // 暂时返回模拟数据
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        id: 1,
        username: 'current_user',
        email: 'user@example.com',
        created_at: new Date().toISOString(),
      })
    }, 200)
  })
}

/**
 * 用户登出
 */
export function logout(): Promise<void> {
  // 登出逻辑在前端处理，清除本地存储
  return Promise.resolve()
}
