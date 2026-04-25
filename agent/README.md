# Engineering AI Agent Backend

工程AI智能体后端服务，基于FastAPI构建的微服务架构。

## 🚀 技术栈

- **Web框架**: FastAPI
- **异步任务**: Celery + Redis
- **向量数据库**: ChromaDB
- **LLM推理**: DeepSeek API
- **嵌入模型**: BAAI/bge-small-zh-v1.5
- **配置管理**: Pydantic Settings + YAML配置

## 📁 项目目录结构

```
backend/
├── app/
│   ├── api/                    # FastAPI路由
│   ├── core/
│   │   ├── config.py           # 环境变量配置 (Pydantic Settings)
│   │   ├── yaml_config.py      # YAML配置加载器
│   │   └── security.py         # API Key认证中间件
│   ├── db/                     # 数据库客户端
│   ├── models/                 # Pydantic请求/响应模型
│   ├── services/               # 业务逻辑层
│   ├── tasks/                  # Celery任务
│   └── main.py                 # FastAPI应用入口
├── data/                       # 持久化数据目录
├── .env                        # 环境变量（不提交）
├── .env.example                # 环境变量模板
├── config.yaml                 # YAML配置文件（可选）
├── config.yaml.example         # YAML配置模板
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## ⚙️ 配置方式

### 方式一：环境变量配置（默认）

使用 `.env` 文件配置所有参数：

```bash
cp .env.example .env
# 编辑 .env 文件，填入您的密钥
```

### 方式二：YAML配置文件（推荐用于复杂部署）

1. 复制YAML配置模板：
```bash
cp config.yaml.example config.yaml
```

2. 编辑 `config.yaml` 文件，配置大模型、数据库等参数

3. YAML配置支持环境变量引用：
```yaml
llm:
  deepseek:
    api_key: "${DEEPSEEK_API_KEY}"  # 从环境变量读取
    model_name: "deepseek-coder"
```

### 配置优先级

1. **YAML配置**（如果存在 `config.yaml` 文件）
2. **环境变量**（`.env` 文件或系统环境变量）

## 🔑 必需的环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | `sk-xxxxxx` |
| `API_KEY` | 应用API密钥 | `your_app_secret_key` |
| `SECRET_KEY` | JWT密钥 | `your-secret-key` |

## 🐳 Docker部署

```bash
# 构建镜像
docker build -t eng-ai-backend .

# 使用docker-compose启动
docker-compose up -d
```

## 🏃 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动Redis（需要单独安装）
redis-server

# 启动Celery Worker
celery -A app.tasks.worker worker --loglevel=info

# 启动FastAPI
uvicorn app.main:app --reload
```

## 📡 API接口

- `POST /upload/` - 文档上传
- `GET /upload/task/{task_id}` - 任务状态查询
- `POST /query/` - RAG问答
- `POST /report/` - 报告生成
- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `GET /files/` - 文件列表
- `GET /download/{filename}` - 文件下载
- `GET /health` - 健康检查

## 📚 文档

- [架构设计文档](ARCHITECTURE.md)
- [部署指南](DEPLOYMENT.md)
- [项目总结](PROJECT_SUMMARY.md)
