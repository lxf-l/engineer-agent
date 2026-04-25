from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import Optional
from app.models.schemas import UploadResponse, TaskStatusResponse
from app.services.document_service import DocumentService
from app.tasks.document_tasks import get_task_status
from app.core.security import verify_api_key
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/upload",
    tags=["文档上传"],
    responses={401: {"description": "Unauthorized"}}
)


@router.post(
    "/",
    response_model=UploadResponse,
    summary="上传文档并启动处理",
    description="上传PDF、DOCX或TXT文档，系统将异步进行解析、分块和向量化处理"
)
async def upload_document(
    file: UploadFile = File(..., description="要上传的文档文件"),
    collection_name: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    上传文档并启动异步处理任务
    
    - **file**: 要上传的文件（支持PDF、DOCX、TXT）
    - **collection_name**: 可选的集合名称，默认使用配置中的集合
    """
    # 验证文件类型
    if not DocumentService.validate_file_type(file.filename or ""):
        raise HTTPException(
            status_code=400,
            detail="不支持的文件类型。仅支持 PDF、DOCX、TXT 格式"
        )
    
    # 保存文件并启动处理
    result = await DocumentService.save_upload_file(
        file=file,
        collection_name=collection_name
    )
    
    return UploadResponse(**result)


@router.get(
    "/task/{task_id}",
    response_model=TaskStatusResponse,
    summary="查询任务状态",
    description="根据任务ID查询文档处理的进度和状态"
)
async def get_task_progress(
    task_id: str,
    api_key: str = Depends(verify_api_key)
):
    """
    查询任务状态
    
    - **task_id**: 任务ID
    """
    try:
        status_info = get_task_status(task_id)
        return TaskStatusResponse(**status_info)
    except Exception as e:
        logger.error(f"Failed to get task status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"查询任务状态失败: {str(e)}"
        )
