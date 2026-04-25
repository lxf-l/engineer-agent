"""YAML configuration loader for Engineering AI Agent"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """大语言模型配置"""
    model_name: str
    api_key: str
    base_url: str
    timeout: int = 30
    max_retries: int = 3


class DeepSeekConfig(LLMConfig):
    """DeepSeek特定配置"""
    pass


class OpenAIConfig(LLMConfig):
    """OpenAI特定配置"""
    pass


class EmbeddingConfig(BaseModel):
    """嵌入模型配置"""
    model_name: str = "BAAI/bge-small-zh-v1.5"
    device: str = "cpu"
    batch_size: int = 32
    normalize_embeddings: bool = True


class ChromaConfig(BaseModel):
    """ChromaDB配置"""
    persist_directory: str
    collection_name: str = "engineering_docs"
    distance_metric: str = "cosine"
    embedding_function: str = "default"


class DatabaseConfig(BaseModel):
    """数据库配置基类"""
    url: str
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10


class RedisConfig(BaseModel):
    """Redis配置"""
    url: str
    max_connections: int = 10
    retry_on_timeout: bool = True
    health_check_interval: int = 30


class FileUploadConfig(BaseModel):
    """文件上传配置"""
    upload_directory: str
    allowed_extensions: list = [".pdf", ".docx", ".doc", ".txt"]
    max_file_size: int = 10485760  # 10MB
    chunk_size: int = 600
    chunk_overlap: int = 100


class JWTConfig(BaseModel):
    """JWT配置"""
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


class SecurityConfig(BaseModel):
    """安全配置"""
    api_key: str
    jwt: JWTConfig


class ServerConfig(BaseModel):
    """服务器配置"""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    workers: int = 1


class CeleryConfig(BaseModel):
    """Celery配置"""
    broker_url: str
    result_backend: str
    task_serializer: str = "json"
    accept_content: list = ["json"]
    result_serializer: str = "json"
    timezone: str = "Asia/Shanghai"
    enable_utc: bool = True
    worker_concurrency: int = 2


class RAGConfig(BaseModel):
    """RAG配置"""
    top_k: int = 5
    similarity_threshold: float = 0.7
    max_context_length: int = 2000


class LoggingConfig(BaseModel):
    """日志配置"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "./logs/app.log"


class YAMLSettings(BaseModel):
    """YAML配置设置"""
    llm: Dict[str, Any]
    embedding: EmbeddingConfig
    vector_database: Dict[str, Any]
    database: Dict[str, Any]
    redis: RedisConfig
    file_upload: FileUploadConfig
    security: SecurityConfig
    server: ServerConfig
    celery: CeleryConfig
    rag: RAGConfig
    logging: LoggingConfig

    @classmethod
    def from_yaml(cls, yaml_path: str = "config.yaml") -> "YAMLSettings":
        """从YAML文件加载配置"""
        config_path = Path(yaml_path)
        if not config_path.exists():
            raise FileNotFoundError(f"配置文件 {yaml_path} 不存在")
        
        with open(config_path, "r", encoding="utf-8") as f:
            config_dict = yaml.safe_load(f)
        
        # 替换环境变量
        config_dict = cls._replace_env_vars(config_dict)
        
        return cls(**config_dict)
    
    @staticmethod
    def _replace_env_vars(config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """递归替换配置中的环境变量"""
        def replace_value(value: Any) -> Any:
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                # 提取环境变量名和默认值
                env_var = value[2:-1]  # 移除 ${ 和 }
                if ":" in env_var:
                    var_name, default_value = env_var.split(":", 1)
                    return os.getenv(var_name, default_value)
                else:
                    return os.getenv(env_var, "")
            elif isinstance(value, dict):
                return {k: replace_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [replace_value(v) for v in value]
            else:
                return value
        
        return {k: replace_value(v) for k, v in config_dict.items()}


# 全局配置实例
try:
    yaml_settings = YAMLSettings.from_yaml()
except Exception as e:
    print(f"警告: 无法加载YAML配置文件: {e}")
    yaml_settings = None
