import request from './client'
import type { ReportRequest, ReportResponse } from '@/types'

/**
 * 生成工程报告
 */
export function generateReport(params: ReportRequest): Promise<ReportResponse> {
  return request.post('/report/', params)
}
