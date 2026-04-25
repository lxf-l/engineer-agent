"""File download endpoints for uploaded documents"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from app.services.file_service import FileService


router = APIRouter(prefix="/download", tags=["file download"])


@router.get("/{filename}")
def download_file(filename: str):
    """下载指定文件"""
    try:
        # 验证文件是否存在
        if not FileService.file_exists(filename):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
        
        # 获取文件路径
        upload_dir = FileService.get_upload_dir()
        file_path = upload_dir / filename
        
        # 返回文件响应
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type="application/octet-stream"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件下载失败: {str(e)}"
        )
