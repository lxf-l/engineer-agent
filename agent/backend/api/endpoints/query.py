from fastapi import APIRouter, Depends, HTTPException
from backend.models.schemas import QueryRequest, QueryResponse
from backend.services.rag_service import RAGService
from backend.core.security import verify_api_key
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/query",
    tags=["RAG问答"],
    responses={401: {"description": "Unauthorized"}}
)


@router.post(
    "/",
    response_model=QueryResponse,
    summary="RAG智能问答",
    description="基于向量数据库的检索增强生成问答，支持工程技术领域问题"
)
async def query_documents(
    request: QueryRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    执行RAG问答
    
    - **question**: 用户提出的问题
    - **top_k**: 检索的文档片段数量（默认5，范围1-20）
    - **collection_name**: 可选的集合名称
    """
    try:
        # 初始化RAG服务
        rag_service = RAGService()
        
        # 执行查询
        result = rag_service.query(
            question=request.question,
            top_k=request.top_k,
            collection_name=request.collection_name
        )
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"查询处理失败: {str(e)}"
        )
