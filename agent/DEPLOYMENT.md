# Engineering AI Agent Backend - 部署与运维指南

## 📋 部署前检查清单

### 1. 环境准备

- [ ] Python 3.9+ 已安装（本地开发）
- [ ] Docker 20.10+ 已安装
- [ ] Docker Compose 2.0+ 已安装
- [ ] Redis 7.0+ 已安装（本地开发，如不使用Docker）

### 2. 配置文件

- [ ] `.env` 文件已从 `.env.example` 复制
- [ ] `DEEPSEEK_API_KEY` 已配置有效的DeepSeek API密钥
- [ ] `API_KEY` 已设置强密码（建议16位以上）
- [ ] `REDIS_URL` 配置正确
- [ ] `CHROMA_PERSIST_DIR` 和 `UPLOAD_DIR` 路径存在且可写

### 3. 依赖安装

**本地开发**:
```bash
pip install -r requirements.txt
```

**Docker部署**:
```bash
docker-compose build
```

### 4. 网络端口

确保以下端口未被占用：
- [ ] 8000 (FastAPI)
- [ ] 6379 (Redis)

### 5. 磁盘空间

- [ ] 至少5GB可用空间（Docker镜像 + 数据）
- [ ] 预计每个1000个文档需要1GB存储空间

## 🚀 部署步骤

### 方式一：Docker Compose（推荐生产环境）

#### Step 1: 准备环境变量

```bash
cp .env.example .env
# 编辑.env文件，填入真实配置
nano .env
```

#### Step 2: 构建并启动服务

```bash
# 首次启动（会自动构建镜像）
docker-compose up -d

# 或者先构建再启动
docker-compose build
docker-compose up -d
```

#### Step 3: 验证部署

```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 测试健康检查
curl http://localhost:8000/health
```

#### Step 4: 运行测试（可选）

```bash
# 安装Python requests库
pip install requests

# 运行API测试
python test_api.py
```

### 方式二：本地运行（适合开发调试）

#### Step 1: 启动Redis

```bash
# Linux/Mac
redis-server

# Windows (需要安装Redis)
redis-server.exe
```

#### Step 2: 配置环境变量

```bash
cp .env.example .env
# 编辑.env文件
```

#### Step 3: 安装依赖

```bash
pip install -r requirements.txt
```

#### Step 4: 启动Celery Worker

```bash
# 在终端窗口1中运行
celery -A app.tasks.worker worker --loglevel=info --concurrency=2
```

#### Step 5: 启动FastAPI应用

```bash
# 在终端窗口2中运行
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 6: 访问API文档

打开浏览器访问: http://localhost:8000/docs

## 🔧 运维管理

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f celery-worker
docker-compose logs -f redis

# 实时日志（最后100行）
docker-compose logs --tail=100 backend
```

### 服务重启

```bash
# 重启所有服务
docker-compose restart

# 重启单个服务
docker-compose restart backend
docker-compose restart celery-worker
```

### 服务停止

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷（谨慎使用！）
docker-compose down -v
```

### 扩容Worker

```bash
# 增加Celery Worker实例数
docker-compose up -d --scale celery-worker=3
```

## 📊 监控与告警

### 健康检查

**端点**: `GET /health`

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "version": "1.0.0"
}
```

### 关键指标监控

建议监控以下指标：

1. **API响应时间**: P95 < 2s
2. **Celery任务队列长度**: < 100
3. **ChromaDB文档数量**: 根据业务需求
4. **磁盘使用率**: < 80%
5. **内存使用率**: < 85%

### 日志级别

- `DEBUG`: 开发环境
- `INFO`: 生产环境（默认）
- `WARNING`: 仅警告
- `ERROR`: 仅错误

修改`.env`中的`DEBUG=true/false`来控制日志级别。

## 🐛 故障排查

### 问题1: Celery Worker无法连接Redis

**症状**:
```
ConnectionError: Error connecting to Redis
```

**解决方案**:
```bash
# 检查Redis是否运行
docker-compose ps redis

# 检查网络连接
docker exec -it eng-ai-celery-worker ping redis

# 检查REDIS_URL配置
cat .env | grep REDIS_URL
```

### 问题2: 文档上传失败

**症状**:
```
Failed to save upload file
```

**解决方案**:
```bash
# 检查目录权限
ls -la data/uploads

# 创建目录并设置权限
mkdir -p data/uploads
chmod 755 data/uploads
```

### 问题3: ChromaDB初始化失败

**症状**:
```
Failed to initialize ChromaDB
```

**解决方案**:
```bash
# 检查持久化目录
ls -la data/chroma

# 清空ChromaDB数据（会删除所有索引！）
rm -rf data/chroma/*
docker-compose restart backend
```

### 问题4: DeepSeek API调用失败

**症状**:
```
AuthenticationError: Invalid API key
```

**解决方案**:
```bash
# 验证API Key
cat .env | grep DEEPSEEK_API_KEY

# 测试DeepSeek API
curl -H "Authorization: Bearer YOUR_DEEPSEEK_KEY" \
  https://api.deepseek.com/v1/chat/completions
```

### 问题5: 内存不足

**症状**:
```
Killed process or OOM error
```

**解决方案**:
```bash
# 限制Worker并发数
# 编辑docker-compose.yml，修改:
command: celery -A app.tasks.worker worker --loglevel=info --concurrency=1

# 增加Docker内存限制
# 在docker-compose.yml中添加:
deploy:
  resources:
    limits:
      memory: 2G
```

## 🔒 安全加固

### 1. 生产环境配置

**.env文件**:
```env
DEBUG=false                    # 关闭调试模式
API_KEY=<强密码>               # 至少16位
DEEPSEEK_API_KEY=<真实密钥>    # 从DeepSeek控制台获取
```

### 2. CORS配置

修改`app/main.py`，限制允许的域名：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # 限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. HTTPS配置

使用Nginx反向代理 + Let's Encrypt证书：

```nginx
server {
    listen 443 ssl;
    server_name api.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. 速率限制

添加慢速API限制（需要使用中间件）：

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

## 📈 性能优化

### 1. 向量检索优化

调整检索参数：

```env
# .env文件
CHUNK_SIZE=800          # 增大自然语言上下文
CHUNK_OVERLAP=150       # 增加重叠保持连贯性
RAG_TOP_K=7            # 根据实际需求调整
```

### 2. Celery优化

**预取控制**:
```python
# app/tasks/worker.py
worker_prefetch_multiplier=1  # 每次只处理一个任务
```

**并发度**:
```yaml
# docker-compose.yml
command: celery -A app.tasks.worker worker --concurrency=2
```

### 3. 数据库优化

**批量插入**:
```python
# 在vector_store.py中批量添加
vector_store.add_documents(
    documents=documents,  # 批量而非逐个
    metadatas=metadatas,
    ids=ids
)
```

## 🔄 备份与恢复

### 数据备份

```bash
# 备份ChromaDB数据
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz data/chroma/

# 备份上传文件
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz data/uploads/
```

### 数据恢复

```bash
# 恢复ChromaDB数据
tar -xzf chroma_backup_20240101.tar.gz
docker-compose restart backend
```

## 📦 版本升级

### 更新依赖

```bash
# 更新Python依赖
pip install --upgrade -r requirements.txt

# 重新构建Docker镜像
docker-compose build --no-cache
docker-compose up -d
```

### 迁移数据

新版本如果更改了ChromaDB schema，可能需要重新索引：

```bash
# 备份旧数据
mv data/chroma data/chroma_old

# 启动新版本
docker-compose up -d

# 重新上传文档
python test_api.py
```

---

**文档版本**: 1.0.0  
**最后更新**: 2024-01-01  
**维护者**: Engineering AI Team
