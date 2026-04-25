import os
import uuid
from pathlib import Path
from typing import List, Dict, Any
from celery.result import AsyncResult
from app.tasks.worker import celery_app
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.db.vector_store import vector_store
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def process_document(self, file_path: str, filename: str, collection_name: str):
    """
    异步处理文档：解析、分块、向量化并存储
    
    Args:
        file_path: 文件路径
        filename: 文件名
        collection_name: 集合名称
    """
    try:
        logger.info(f"Starting to process document: {filename}")
        
        # 更新任务状态：开始解析
        self.update_state(state="PROCESSING", meta={"step": "parsing", "progress": 10})
        
        # 1. 加载文档
        documents = load_document(file_path)
        if not documents:
            raise ValueError("无法解析文档内容")
        
        logger.info(f"Document loaded, pages: {len(documents)}")
        
        # 更新任务状态：开始分块
        self.update_state(state="PROCESSING", meta={"step": "splitting", "progress": 30})
        
        # 2. 文本分块
        chunks = split_text(documents)
        logger.info(f"Document split into {len(chunks)} chunks")
        
        # 更新任务状态：开始向量化
        self.update_state(state="PROCESSING", meta={"step": "embedding", "progress": 50})
        
        # 3. 向量化并存储
        store_embeddings(chunks, filename, collection_name)
        logger.info(f"Embeddings stored successfully")
        
        # 更新任务状态：完成
        return {
            "status": "completed",
            "filename": filename,
            "chunks": len(chunks),
            "step": "completed",
            "progress": 100
        }
        
    except Exception as e:
        logger.error(f"Failed to process document: {e}", exc_info=True)
        self.update_state(
            state="FAILED",
            meta={
                "step": "error",
                "error": str(e)
            }
        )
        raise


def load_document(file_path: str) -> List:
    """
    根据文件类型加载文档
    
    Args:
        file_path: 文件路径
        
    Returns:
        文档列表
    """
    ext = Path(file_path).suffix.lower()
    
    try:
        if ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext in ['.docx', '.doc']:
            loader = Docx2txtLoader(file_path)
        elif ext == '.txt':
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"不支持的文件类型: {ext}")
        
        return loader.load()
        
    except Exception as e:
        logger.error(f"Failed to load document: {e}")
        raise


def split_text(documents: List, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
    """
    使用递归字符分割器分块
    
    Args:
        documents: 文档列表
        chunk_size: 分块大小
        chunk_overlap: 分块重叠大小
        
    Returns:
        文本块列表
    """
    if chunk_size is None:
        chunk_size = settings.CHUNK_SIZE
    if chunk_overlap is None:
        chunk_overlap = settings.CHUNK_OVERLAP
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # 提取纯文本内容
    return [chunk.page_content for chunk in chunks]


def store_embeddings(chunks: List[str], filename: str, collection_name: str):
    """
    将文本块向量化并存储到ChromaDB
    
    Args:
        chunks: 文本块列表
        filename: 文件名
        collection_name: 集合名称
    """
    # 初始化嵌入模型
    embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    
    documents = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        doc_id = f"{filename}_{uuid.uuid4().hex[:8]}_{i}"
        
        documents.append(chunk)
        metadatas.append({
            "source": filename,
            "chunk_index": i,
            "total_chunks": len(chunks)
        })
        ids.append(doc_id)
    
    # 批量添加到向量数据库
    vector_store.add_documents(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
        collection_name=collection_name
    )


def get_task_status(task_id: str) -> Dict[str, Any]:
    """
    获取任务状态
    
    Args:
        task_id: 任务ID
        
    Returns:
        任务状态信息
    """
    result = AsyncResult(task_id, app=celery_app)
    
    response = {
        "task_id": task_id,
        "status": result.status,
    }
    
    if result.status == "SUCCESS":
        response.update(result.result)
    elif result.status == "FAILURE":
        response["error"] = str(result.result)
    elif result.status == "PROCESSING":
        if hasattr(result.result, 'meta'):
            response.update(result.result.meta)
    
    return response
