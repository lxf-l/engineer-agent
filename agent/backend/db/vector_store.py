import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB向量存储单例封装"""
    
    _instance = None
    _client = None
    _collection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._initialize()
    
    def _initialize(self):
        """初始化ChromaDB客户端和集合"""
        try:
            # 创建持久化客户端
            self._client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
                settings=ChromaSettings(
                    anonymized_telemetry=False
                )
            )
            
            # 获取或创建集合
            self._collection = self._client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                metadata={"description": "Engineering documents collection"}
            )
            
            logger.info(f"ChromaDB initialized with collection: {settings.CHROMA_COLLECTION_NAME}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    @property
    def client(self):
        """获取ChromaDB客户端"""
        return self._client
    
    @property
    def collection(self):
        """获取默认集合"""
        return self._collection
    
    def get_collection(self, collection_name: Optional[str] = None):
        """
        获取指定集合
        
        Args:
            collection_name: 集合名称，默认使用配置中的集合
            
        Returns:
            Collection对象
        """
        if collection_name:
            return self._client.get_or_create_collection(name=collection_name)
        return self._collection
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str],
        collection_name: Optional[str] = None
    ):
        """
        添加文档到向量数据库
        
        Args:
            documents: 文档内容列表
            metadatas: 元数据列表
            ids: 文档ID列表
            collection_name: 集合名称（可选）
        """
        collection = self.get_collection(collection_name)
        
        # ChromaDB会自动处理嵌入（如果配置了嵌入函数）
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Added {len(documents)} documents to collection")
    
    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
        collection_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        相似度搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            collection_name: 集合名称（可选）
            
        Returns:
            搜索结果列表，每个结果包含document, metadata, distance
        """
        collection = self.get_collection(collection_name)
        
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # 整理返回结果
        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                'id': results['ids'][0][i],
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if results['distances'] else None
            })
        
        return formatted_results
    
    def delete_collection(self, collection_name: str):
        """
        删除集合
        
        Args:
            collection_name: 集合名称
        """
        try:
            self._client.delete_collection(name=collection_name)
            logger.info(f"Deleted collection: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            raise
    
    def get_collection_count(self, collection_name: Optional[str] = None) -> int:
        """
        获取集合中文档数量
        
        Args:
            collection_name: 集合名称（可选）
            
        Returns:
            文档数量
        """
        collection = self.get_collection(collection_name)
        return collection.count()


# 全局单例
vector_store = VectorStore()
