import os
import time
from typing import List, Dict, Any, Optional
from langchain_deepseek import ChatDeepSeek
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.db.vector_store import vector_store
import logging

logger = logging.getLogger(__name__)


class RAGService:
    """RAG检索增强生成服务"""
    
    def __init__(self):
        # 初始化嵌入模型
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        # 初始化LLM
        self.llm = ChatDeepSeek(
            api_key=settings.DEEPSEEK_API_KEY,
            model_name="deepseek-chat",
            temperature=0.7
        )
    
    def query(
        self,
        question: str,
        top_k: int = 5,
        collection_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        执行RAG查询
        
        Args:
            question: 用户问题
            top_k: 检索的文档片段数量
            collection_name: 集合名称（可选）
            
        Returns:
            包含answer、sources、processing_time_ms的字典
        """
        start_time = time.time()
        
        try:
            # 1. 将问题向量化并检索
            logger.info(f"Searching for: {question}")
            search_results = vector_store.similarity_search(
                query=question,
                top_k=top_k,
                collection_name=collection_name
            )
            
            if not search_results:
                return {
                    "answer": "抱歉，没有找到相关的参考文档。",
                    "sources": [],
                    "processing_time_ms": int((time.time() - start_time) * 1000)
                }
            
            # 2. 整理来源文档
            sources = []
            context_parts = []
            
            for i, result in enumerate(search_results, 1):
                source_info = {
                    "content": result['document'][:200],  # 截取前200字符
                    "source": result['metadata'].get('source', 'Unknown'),
                    "page": result['metadata'].get('page'),
                    "similarity": round(1.0 - (result['distance'] or 0), 2) if result['distance'] else None
                }
                sources.append(source_info)
                
                # 构建上下文
                context_parts.append(
                    f"[文档 {i}] (来源: {source_info['source']}, "
                    f"页码: {source_info['page'] or 'N/A'}, "
                    f"相似度: {source_info['similarity']})\n"
                    f"{result['document']}\n"
                )
            
            # 3. 构建Prompt
            context_text = "\n".join(context_parts)
            system_prompt = f"""你是一个专业的工程技术助手，请根据提供的参考文档回答问题。
如果参考文档中没有相关信息，请明确说明。回答要专业、准确、简洁。

参考文档：
{context_text}

请回答以下问题：
{question}

答案："""
            
            # 4. 调用LLM生成答案
            logger.info("Generating answer with DeepSeek...")
            response = self.llm.invoke(system_prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            processing_time = int((time.time() - start_time) * 1000)
            
            logger.info(f"Query completed in {processing_time}ms")
            
            return {
                "answer": answer,
                "sources": sources,
                "processing_time_ms": processing_time
            }
            
        except Exception as e:
            logger.error(f"Error in RAG query: {e}", exc_info=True)
            processing_time = int((time.time() - start_time) * 1000)
            return {
                "answer": f"查询处理时发生错误: {str(e)}",
                "sources": [],
                "processing_time_ms": processing_time
            }
