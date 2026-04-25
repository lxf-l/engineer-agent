import request from './client'
import type { UploadResponse, TaskStatusResponse } from '@/types'

/**
 * 上传文档
 */
export function uploadDocument(file: File, collectionName?: string): Promise<UploadResponse> {
  const formData = new FormData()
  formData.append('file', file)
  if (collectionName) {
    formData.append('collection_name', collectionName)
  }

  return request.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

/**
 * 查询任务状态
 */
export function getTaskStatus(taskId: string): Promise<TaskStatusResponse> {
  return request.get(`/upload/task/${taskId}`)
}

/**
 * 获取文件列表
 */
export function getFileList(): Promise<any> {
  return request.get('/files/')
}

/**
 * 获取文件信息
 */
export function getFileInfo(filename: string): Promise<any> {
  return request.get(`/files/${filename}`)
}

/**
 * 删除文件
 */
export function deleteFile(filename: string): Promise<any> {
  return request.delete(`/files/${filename}`)
}

/**
 * 下载文件
 */
export function downloadFile(filename: string): Promise<Blob> {
  return request.get(`/download/${filename}`, {
    responseType: 'blob'
  })
}
