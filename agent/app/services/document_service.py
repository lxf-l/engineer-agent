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
    
    # 支持的文件类型
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def _validate_file(file: UploadFile) -> None:
        """验证上传的文件"""
        # 检查文件扩展名
        if file.filename:
            ext = Path(file.filename).suffix.lower()
            if ext not in DocumentService.ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"不支持的文件类型。支持的类型: {', '.join(DocumentService.ALLOWED_EXTENSIONS)}"
                )
        
        # 检查文件大小（需要读取内容）
        # 注意：FastAPI的UploadFile在异步上下文中可能无法直接获取size
        # 这里我们先保存再检查，或者在前端限制
        
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
            # 验证文件
            DocumentService._validate_file(file)
            
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
            
            # 记录文件信息
            logger.info(f"文件保存成功: {file_path}")
            
            # 启动异步处理任务
            task = process_document.delay(
                str(file_path),
                file_path.name,
                collection_name or settings.CHROMA_COLLECTION_NAME
            )
            
            return {
                "task_id": task.id,
                "status": "pending",
                "filename": file_path.name
            }
            
        except Exception as e:
            logger.error(f"文件保存失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")
