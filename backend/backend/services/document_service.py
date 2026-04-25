import os
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from typing import Optional
import logging
from app.core.config import settings
from app.tasks.document_tasks import process_document

logger = logging.getLogger(__name__)


class DocumentService:
    """文档处理服务类"""
    
    @staticmethod
    async def save_upload_file(
        file: UploadFile,
        collection_name: Optional[str] = None
    ) -> dict:
        """
        保存上传的文件并启动异步处理任务
        
        Args:
            file: 上传的文件对象
            collection_name: 集合名称（可选）
            
        Returns:
            包含task_id、status、filename的字典
            
        Raises:
            HTTPException: 文件保存失败时抛出
        """
        try:
            # 确保上传目录存在
            upload_dir = Path(settings.UPLOAD_DIR)
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            # 生成安全的文件名
            filename = file.filename or "unnamed_file"
            file_path = upload_dir / filename
            
            # 检查文件是否已存在，如果存在则添加序号
            counter = 1
            while file_path.exists():
                name_parts = filename.rsplit('.', 1)
                if len(name_parts) == 2:
                    new_filename = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                else:
                    new_filename = f"{filename}_{counter}"
                file_path = upload_dir / new_filename
                counter += 1
            
            # 保存文件
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            logger.info(f"File saved: {file_path}")
            
            # 启动Celery异步任务
            task = process_document.delay(
                file_path=str(file_path),
                filename=filename,
                collection_name=collection_name or settings.CHROMA_COLLECTION_NAME
            )
            
            return {
                "task_id": task.id,
                "status": "pending",
                "filename": filename
            }
            
        except Exception as e:
            logger.error(f"Failed to save upload file: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process file: {str(e)}"
            )
    
    @staticmethod
    def validate_file_type(filename: str) -> bool:
        """
        验证文件类型是否支持
        
        Args:
            filename: 文件名
            
        Returns:
            是否为支持的类型
        """
        allowed_extensions = {'.pdf', '.docx', '.doc', '.txt'}
        ext = Path(filename).suffix.lower()
        return ext in allowed_extensions
