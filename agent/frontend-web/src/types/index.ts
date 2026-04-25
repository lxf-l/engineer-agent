// 用户相关类型
export interface User {
  id: number
  username: string
  email: string
  created_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  confirm_password?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface RefreshTokenRequest {
  refresh_token: string
}

// 文件管理相关类型
export interface FileInfo {
  filename: string
  size: number
  created_at: number
  modified_at: number
  path: string
}

export interface FileListResponse {
  files: FileInfo[]
}

export interface DeleteFileResponse {
  success: boolean
  message: string
}

// 文档上传相关类型
export interface UploadRequest {
  collection_name?: string
}

export interface UploadResponse {
  task_id: string
  status: string
  filename: string
}

export interface TaskStatusResponse {
  task_id: string
  status: string
  filename?: string
  step?: string
  chunks?: number
  error?: string
  created_at?: string
}

// RAG问答相关类型
export interface QueryRequest {
  question: string
  top_k?: number
  collection_name?: string
}

export interface SourceDocument {
  content: string
  source: string
  page?: number
  similarity?: number
}

export interface QueryResponse {
  answer: string
  sources: SourceDocument[]
  processing_time_ms: number
}

// 报告生成相关类型
export interface ReportRequest {
  report_type: string
  parameters: Record<string, any>
  collection_name?: string
}

export interface ReportReference {
  standard_name: string
  section?: string
  content?: string
}

export interface ReportResponse {
  content: string
  references: ReportReference[]
  generated_at: string
}

// 健康检查
export interface HealthResponse {
  status: string
  timestamp: string
  version: string
}

// 通用响应类型
export interface ApiResponse<T = any> {
  code?: number
  message?: string
  data: T
}
