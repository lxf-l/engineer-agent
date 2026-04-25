"""File management service for handling uploaded documents"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import HTTPException
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class FileService:
    """文件管理服务类"""
    
    @staticmethod
    def get_upload_dir() -> Path:
        """获取上传目录路径"""
        return Path(settings.UPLOAD_DIR)
    
    @staticmethod
    def list_files() -> List[dict]:
        """列出所有上传的文件"""
        upload_dir = FileService.get_upload_dir()
        if not upload_dir.exists():
            return []
        
        files = []
        for file_path in upload_dir.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "created_at": stat.st_ctime,
                    "modified_at": stat.st_mtime,
                    "path": str(file_path)
                })
        
        # 按创建时间排序（最新在前）
        files.sort(key=lambda x: x["created_at"], reverse=True)
        return files
    
    @staticmethod
    def get_file_info(filename: str) -> dict:
        """获取指定文件的信息"""
        upload_dir = FileService.get_upload_dir()
        file_path = upload_dir / filename
        
        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        stat = file_path.stat()
        return {
            "filename": filename,
            "size": stat.st_size,
            "created_at": stat.st_ctime,
            "modified_at": stat.st_mtime,
            "path": str(file_path)
        }
    
    @staticmethod
    def delete_file(filename: str) -> bool:
        """删除指定文件"""
        upload_dir = FileService.get_upload_dir()
        file_path = upload_dir / filename
        
        if not file_path.exists() or not file_path.is_file():
            return False
        
        try:
            file_path.unlink()
            logger.info(f"文件删除成功: {file_path}")
            return True
        except Exception as e:
            logger.error(f"文件删除失败: {str(e)}")
            return False
    
    @staticmethod
    def file_exists(filename: str) -> bool:
        """检查文件是否存在"""
        upload_dir = FileService.get_upload_dir()
        file_path = upload_dir / filename
        return file_path.exists() and file_path.is_file()
