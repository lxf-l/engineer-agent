from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============= 文档上传相关 =============

class UploadResponse(BaseModel):
    """文档上传响应模型"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")
    filename: str = Field(..., description="文件名")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "abc123",
                "status": "pending",
                "filename": "document.pdf"
            }
        }


class TaskStatusResponse(BaseModel):
    """任务状态查询响应模型"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态: pending/processing/completed/failed")
    filename: Optional[str] = Field(None, description="文件名")
    step: Optional[str] = Field(None, description="当前处理步骤")
    chunks: Optional[int] = Field(None, description="文档分块数量")
    error: Optional[str] = Field(None, description="错误信息")
    created_at: Optional[str] = Field(None, description="创建时间")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "abc123",
                "status": "completed",
                "filename": "document.pdf",
                "step": "completed",
                "chunks": 45,
                "error": None,
                "created_at": "2024-01-01T12:00:00"
            }
        }


# ============= RAG问答相关 =============

class QueryRequest(BaseModel):
    """RAG问答请求模型"""
    question: str = Field(..., description="用户问题", min_length=1)
    top_k: Optional[int] = Field(5, description="检索的文档片段数量", ge=1, le=20)
    collection_name: Optional[str] = Field(None, description="集合名称，默认使用配置中的集合")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "C30混凝土的配合比是什么？",
                "top_k": 5,
                "collection_name": "engineering_docs"
            }
        }


class SourceDocument(BaseModel):
    """来源文档模型"""
    content: str = Field(..., description="文档片段内容")
    source: str = Field(..., description="来源文件名")
    page: Optional[int] = Field(None, description="页码")
    similarity: Optional[float] = Field(None, description="相似度分数")
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "C30混凝土配合比设计...",
                "source": "concrete_standard.pdf",
                "page": 15,
                "similarity": 0.89
            }
        }


class QueryResponse(BaseModel):
    """RAG问答响应模型"""
    answer: str = Field(..., description="LLM生成的答案")
    sources: List[SourceDocument] = Field(default_factory=list, description="引用的来源文档")
    processing_time_ms: int = Field(..., description="处理时间（毫秒）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "C30混凝土的配合比通常为...",
                "sources": [],
                "processing_time_ms": 1250
            }
        }


# ============= 报告生成相关 =============

class ReportType(str):
    """报告类型枚举"""
    CONCRETE_MIX = "concrete_mix"
    STRUCTURAL_DESIGN = "structural_design"
    LOAD_CALCULATION = "load_calculation"
    MATERIAL_SPEC = "material_spec"


class ReportRequest(BaseModel):
    """报告生成请求模型"""
    report_type: str = Field(..., description="报告类型")
    parameters: Dict[str, Any] = Field(..., description="报告参数")
    collection_name: Optional[str] = Field(None, description="集合名称")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_type": "concrete_mix",
                "parameters": {
                    "strength_grade": "C30",
                    "slump": "160mm",
                    "environment": "室内干燥环境"
                }
            }
        }


class ReportReference(BaseModel):
    """报告引用规范模型"""
    standard_name: str = Field(..., description="规范名称")
    section: Optional[str] = Field(None, description="章节")
    content: Optional[str] = Field(None, description="引用内容")
    
    class Config:
        json_schema_extra = {
            "example": {
                "standard_name": "GB 50010-2010",
                "section": "第4.2节",
                "content": "混凝土强度等级规定..."
            }
        }


class ReportResponse(BaseModel):
    """报告生成响应模型"""
    content: str = Field(..., description="生成的报告内容")
    references: List[ReportReference] = Field(default_factory=list, description="引用的规范列表")
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="生成时间")
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "根据工程设计要求...",
                "references": [],
                "generated_at": "2024-01-01T12:00:00"
            }
        }


# ============= 健康检查 =============

class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="时间戳")
    version: str = Field(default="1.0.0", description="版本号")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-01T12:00:00",
                "version": "1.0.0"
            }
        }
