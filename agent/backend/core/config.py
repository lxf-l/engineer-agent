from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置管理类"""
    
    # DeepSeek Configuration
    DEEPSEEK_API_KEY: str
    
    # Application Security
    API_KEY: str
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # ChromaDB Configuration
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    
    # File Upload Configuration
    UPLOAD_DIR: str = "./data/uploads"
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set default Celery URLs if not provided
        if not self.CELERY_BROKER_URL:
            self.CELERY_BROKER_URL = self.REDIS_URL
        if not self.CELERY_RESULT_BACKEND:
            self.CELERY_RESULT_BACKEND = self.REDIS_URL


# Global settings instance
settings = Settings()
