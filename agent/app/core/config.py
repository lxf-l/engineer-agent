from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import model_validator
import os

# 尝试导入 yaml_settings，如果失败则设为 None
try:
    from app.core.yaml_config import yaml_settings
except ImportError:
    yaml_settings = None


class Settings(BaseSettings):
    """应用配置管理类"""
    
    # DeepSeek Configuration
    DEEPSEEK_API_KEY: str = ""
    
    # Application Security
    API_KEY: str = ""
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # ChromaDB Configuration
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    
    # File Upload Configuration
    UPLOAD_DIR: str = "./data/uploads"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./data/users.db"
    
    # Debug Mode
    DEBUG: bool = False
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Celery Configuration
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    
    # Chroma Collection Name
    CHROMA_COLLECTION_NAME: str = "engineering_docs"
    
    # Embedding Model
    EMBEDDING_MODEL: str = "BAAI/bge-small-zh-v1.5"
    
    # Document Processing
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 100
    
    # RAG Configuration
    RAG_TOP_K: int = 5
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    @model_validator(mode='after')
    def load_yaml_config_if_available(self):
        """如果 yaml_settings 可用，则优先使用 YAML 配置"""
        if yaml_settings:
            try:
                # DeepSeek Configuration
                if hasattr(yaml_settings, 'llm') and 'deepseek' in yaml_settings.llm:
                    self.DEEPSEEK_API_KEY = yaml_settings.llm["deepseek"].get("api_key", self.DEEPSEEK_API_KEY)
                
                # Application Security
                if hasattr(yaml_settings, 'security'):
                    self.API_KEY = getattr(yaml_settings.security, 'api_key', self.API_KEY)
                    
                    # JWT Configuration
                    if hasattr(yaml_settings.security, 'jwt'):
                        jwt_conf = yaml_settings.security.jwt
                        self.SECRET_KEY = getattr(jwt_conf, 'secret_key', self.SECRET_KEY)
                        self.ALGORITHM = getattr(jwt_conf, 'algorithm', self.ALGORITHM)
                        self.ACCESS_TOKEN_EXPIRE_MINUTES = getattr(jwt_conf, 'access_token_expire_minutes', self.ACCESS_TOKEN_EXPIRE_MINUTES)
                        self.REFRESH_TOKEN_EXPIRE_DAYS = getattr(jwt_conf, 'refresh_token_expire_days', self.REFRESH_TOKEN_EXPIRE_DAYS)

                # Redis Configuration
                if hasattr(yaml_settings, 'redis'):
                    self.REDIS_URL = getattr(yaml_settings.redis, 'url', self.REDIS_URL)
                
                # ChromaDB Configuration
                if hasattr(yaml_settings, 'vector_database') and 'chroma' in yaml_settings.vector_database:
                    chroma_conf = yaml_settings.vector_database["chroma"]
                    self.CHROMA_PERSIST_DIR = chroma_conf.get("persist_directory", self.CHROMA_PERSIST_DIR)
                    self.CHROMA_COLLECTION_NAME = chroma_conf.get("collection_name", self.CHROMA_COLLECTION_NAME)
                
                # File Upload Configuration
                if hasattr(yaml_settings, 'file_upload'):
                    self.UPLOAD_DIR = getattr(yaml_settings.file_upload, 'upload_directory', self.UPLOAD_DIR)
                    self.CHUNK_SIZE = getattr(yaml_settings.file_upload, 'chunk_size', self.CHUNK_SIZE)
                    self.CHUNK_OVERLAP = getattr(yaml_settings.file_upload, 'chunk_overlap', self.CHUNK_OVERLAP)
                
                # Database Configuration
                if hasattr(yaml_settings, 'database') and 'sqlite' in yaml_settings.database:
                    self.DATABASE_URL = yaml_settings.database["sqlite"].get("url", self.DATABASE_URL)
                
                # Debug Mode & Server Configuration
                if hasattr(yaml_settings, 'server'):
                    self.DEBUG = getattr(yaml_settings.server, 'debug', self.DEBUG)
                    self.HOST = getattr(yaml_settings.server, 'host', self.HOST)
                    self.PORT = getattr(yaml_settings.server, 'port', self.PORT)
                
                # Celery Configuration
                if hasattr(yaml_settings, 'celery'):
                    self.CELERY_BROKER_URL = getattr(yaml_settings.celery, 'broker_url', self.CELERY_BROKER_URL)
                    self.CELERY_RESULT_BACKEND = getattr(yaml_settings.celery, 'result_backend', self.CELERY_RESULT_BACKEND)
                
                # Embedding Model
                if hasattr(yaml_settings, 'embedding'):
                    self.EMBEDDING_MODEL = getattr(yaml_settings.embedding, 'model_name', self.EMBEDDING_MODEL)
                
                # RAG Configuration
                if hasattr(yaml_settings, 'rag'):
                    self.RAG_TOP_K = getattr(yaml_settings.rag, 'top_k', self.RAG_TOP_K)
                    
            except Exception as e:
                # 如果 YAML 处理出错，打印警告并继续使用环境变量/默认值
                print(f"Warning: Failed to load YAML settings, falling back to environment variables. Error: {e}")
        
        return self
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set default Celery URLs if not provided
        if not self.CELERY_BROKER_URL:
            self.CELERY_BROKER_URL = self.REDIS_URL
        if not self.CELERY_RESULT_BACKEND:
            self.CELERY_RESULT_BACKEND = self.REDIS_URL


# Global settings instance
settings = Settings()
