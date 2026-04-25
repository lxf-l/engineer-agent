"""File management endpoints for uploaded documents"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.file_service import FileService
from app.models.schemas import FileListResponse, FileInfo, DeleteFileResponse


router = APIRouter(prefix="/files", tags=["file management"])


@router.get("/", response_model=FileListResponse)
def list_files():
    """列出所有上传的文件"""
    try:
        files = FileService.list_files()
        return FileListResponse(files=files)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取文件列表失败: {str(e)}"
        )


@router.get("/{filename}", response_model=FileInfo)
def get_file_info(filename: str):
    """获取指定文件的信息"""
    try:
        file_info = FileService.get_file_info(filename)
        return file_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取文件信息失败: {str(e)}"
        )


@router.delete("/{filename}", response_model=DeleteFileResponse)
def delete_file(filename: str):
    """删除指定文件"""
    try:
        success = FileService.delete_file(filename)
        if success:
            return DeleteFileResponse(success=True, message="文件删除成功")
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在或删除失败"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件删除失败: {str(e)}"
        )
