import request from './client'
import type { QueryRequest, QueryResponse } from '@/types'

/**
 * RAG智能问答
 */
export function queryKnowledge(params: QueryRequest): Promise<QueryResponse> {
  return request.post('/query/', params)
}
