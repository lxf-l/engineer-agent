from celery import Celery
from app.core.config import settings

# 创建Celery应用实例
celery_app = Celery(
    "engineering_agent",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.document_tasks"]
)

# Celery配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 任务最长执行时间1小时
    worker_prefetch_multiplier=1,  # 每次只预取一个任务
)

# 任务路由配置（可选，用于多队列）
celery_app.conf.task_routes = {
    "app.tasks.document_tasks.process_document": {"queue": "document_processing"}
}
