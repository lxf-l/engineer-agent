# Engineering AI Agent Backend - 架构设计文档

## 📐 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                         │
│  (Web Frontend / Mobile App / API Client)                  │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   API Gateway Layer                         │
│              FastAPI Application (main.py)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CORS Middleware                                     │  │
│  │  API Key Authentication (security.py)                │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Upload   │  │ Query    │  │ Report   │
│ Endpoint │  │ Endpoint │  │ Endpoint │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Document │  │ RAG      │  │ Report   │
│ Service  │  │ Service  │  │ Service  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     │             │             │
     ▼             ▼             │
┌──────────────────────┐         │
│   Celery Task Queue  │         │
│  (Redis Broker)      │         │
└────────┬─────────────┘         │
         │                       │
         ▼                       ▼
┌──────────────────────────────────────┐
│        Data Processing Layer         │
│  ┌────────────┐  ┌──────────────┐  │
│  │ Document   │  │ ChromaDB     │  │
│  │ Parser     │  │ Vector Store │  │
│  └────────────┘  └──────────────┘  │
│  ┌────────────┐  ┌──────────────┐  │
│  │ Text       │  │ DeepSeek     │  │
│  │ Splitter   │  │ LLM API      │  │
│  └────────────┘  └──────────────┘  │
└──────────────────────────────────────┘
```

## 🔄 数据流图

### 1. 文档上传与索引流程

```
Client          FastAPI         Celery Worker      ChromaDB
  │                │                  │                │
  │──POST file──>│                  │                │
  │                │──save file──>│                │
  │                │                  │                │
  │<──task_id───│                  │                │
  │                │──delay task──>│                │
  │                │                  │                │
  │──GET status─>│                  │                │
  │                │──get result──>│                │
  │<──status────│                  │                │
  │                │                  │                │
  │                │                  │──parse──>│    │
  │                │                  │──split──>│    │
  │                │                  │──embed──>│    │
  │                │                  │──store──>│    │
  │                │                  │                │
  │──GET status─>│                  │                │
  │                │──get result──>│                │
  │<──completed─│                  │                │
```

### 2. RAG问答流程

```
Client          FastAPI         RAG Service       DeepSeek
  │                │                  │                │
  │──POST query─>│                  │                │
  │                │──call service─>│                │
  │                │                  │                │
  │                │                  │──embed query─>│
  │                │                  │<──vector─────│
  │                │                  │                │
  │                │                  │──search──>│    │
  │                │                  │<──results──│    │
  │                │                  │                │
  │                │                  │──build prompt   │
  │                │                  │──generate──>│   │
  │                │                  │<──answer────│   │
  │                │                  │                │
  │<──response──│                  │                │
```

## 🏛️ 分层架构详解

### 1. 路由层 (API Layer) - `app/api/endpoints/`

**职责**: 
- 接收HTTP请求
- 参数验证
- 认证授权
- 响应格式化

**文件**:
- `upload.py`: 文档上传接口
- `query.py`: RAG问答接口
- `report.py`: 报告生成接口

### 2. 业务层 (Service Layer) - `app/services/`

**职责**:
- 核心业务逻辑
- 服务编排
- 事务管理

**文件**:
- `document_service.py`: 文档保存、任务调度
- `rag_service.py`: 向量检索、LLM调用
- `report_service.py`: 模板渲染、报告生成

### 3. 数据层 (Data Layer) - `app/db/` + `app/tasks/`

**职责**:
- 数据持久化
- 异步任务执行
- 外部服务集成

**文件**:
- `vector_store.py`: ChromaDB封装（单例模式）
- `document_tasks.py`: Celery异步任务

### 4. 核心层 (Core Layer) - `app/core/`

**职责**:
- 配置管理
- 安全认证
- 通用工具

**文件**:
- `config.py`: Pydantic Settings配置
- `security.py`: API Key认证

## 🔧 设计模式应用

### 1. 单例模式 (Singleton Pattern)

**应用场景**: ChromaDB向量存储客户端

```python
class VectorStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**优势**: 
- 确保全局只有一个数据库连接
- 节省资源，避免重复初始化

### 2. 依赖注入 (Dependency Injection)

**应用场景**: FastAPI的Depends机制

```python
async def verify_api_key(x_api_key: str = Header(...)):
    # 验证逻辑
    return x_api_key

@router.post("/query/")
async def query(api_key: str = Depends(verify_api_key)):
    # 自动注入验证后的API Key
```

**优势**:
- 解耦认证逻辑
- 提高可测试性

### 3. 工厂模式 (Factory Pattern)

**应用场景**: 文档加载器选择

```python
def load_document(file_path: str):
    ext = Path(file_path).suffix.lower()
    if ext == '.pdf':
        return PyPDFLoader(file_path)
    elif ext == '.docx':
        return Docx2txtLoader(file_path)
    # ...
```

**优势**:
- 根据文件类型动态创建加载器
- 易于扩展新格式

### 4. 策略模式 (Strategy Pattern)

**应用场景**: 报告模板选择

```python
REPORT_TEMPLATES = {
    "concrete_mix": "...",
    "structural_design": "...",
    # ...
}

template = REPORT_TEMPLATES.get(report_type)
```

**优势**:
- 运行时选择报告类型
- 轻松添加新模板

## 📊 数据库设计

### ChromaDB集合结构

**Collection**: `engineering_docs`

**Document Schema**:
```json
{
  "id": "unique_chunk_id",
  "document": "文本内容",
  "metadata": {
    "source": "filename.pdf",
    "chunk_index": 0,
    "total_chunks": 45
  }
}
```

**嵌入维度**: 512 (BAAI/bge-small-zh-v1.5)

## 🔐 安全设计

### 1. API Key认证

**流程**:
1. 客户端在Header中携带`X-API-Key`
2. FastAPI中间件拦截请求
3. 与`.env`中的API_KEY比对
4. 不匹配则返回401错误

**代码位置**: `app/core/security.py`

### 2. 环境变量隔离

**敏感信息**:
- DEEPSEEK_API_KEY
- API_KEY
- REDIS_URL

**管理方式**: `.env`文件（不提交到Git）

## ⚡ 性能优化

### 1. 异步处理

**Celery异步任务**:
- 文档解析（耗时操作）
- 向量化计算（CPU密集）
- 批量存储（IO密集）

**优势**: 
- 不阻塞HTTP请求
- 支持并发处理
- 可重试机制

### 2. 向量检索优化

**参数调优**:
- `top_k`: 控制检索数量
- `CHUNK_SIZE`: 600字符（平衡上下文和精度）
- `CHUNK_OVERLAP`: 100字符（保持语义连贯）

### 3. 连接池

**ChromaDB单例**: 
- 复用连接
- 减少初始化开销

## 🚀 部署架构

### Docker Compose编排

```
┌─────────────────────────────────────┐
│         Docker Network              │
│                                     │
│  ┌──────────┐  ┌──────────┐        │
│  │ Backend  │──│  Redis   │        │
│  │ :8000    │  │  :6379   │        │
│  └────┬─────┘  └──────────┘        │
│       │                             │
│  ┌────┴─────┐                      │
│  │  Celery  │                      │
│  │  Worker  │                      │
│  └──────────┘                      │
│                                     │
│  Volume: ./data (持久化)            │
└─────────────────────────────────────┘
```

**网络**: `eng-ai-network` (bridge模式)

**数据卷**: 
- `redis_data`: Redis持久化
- `./data`: ChromaDB和上传文件

## 📈 扩展性设计

### 1. 水平扩展

**Celery Worker**:
```bash
# 增加Worker数量
docker-compose up -d --scale celery-worker=3
```

### 2. 多队列支持

**任务路由配置** (`worker.py`):
```python
celery_app.conf.task_routes = {
    "process_document": {"queue": "document_processing"},
    "generate_report": {"queue": "report_generation"}
}
```

### 3. 微服务拆分

未来可拆分为独立服务:
- Document Service（文档管理服务）
- RAG Service（问答服务）
- Report Service（报告服务）

通过gRPC或消息队列通信

---

**文档版本**: 1.0.0  
**最后更新**: 2024-01-01
