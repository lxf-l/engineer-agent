# Engineering AI Agent - 快速启动指南

## 🚀 完整系统启动（前后端）

### 前置要求

- Docker 20.10+ 和 Docker Compose 2.0+
- Node.js 20+ (如果本地开发)
- Python 3.9+ (如果本地开发)
- Redis 7.0+ (或使用Docker)

---

## 方式一：Docker Compose一键启动（推荐）

### Step 1: 准备后端服务

```bash
# 进入后端目录
cd backend

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入DEEPSEEK_API_KEY和API_KEY
```

### Step 2: 启动后端

```bash
# 在backend目录下
docker-compose up -d

# 验证后端服务
curl http://localhost:8000/health
```

### Step 3: 启动前端

```bash
# 新开终端，进入前端目录
cd frontend-web

# 方式A: Docker方式
docker build -t eng-ai-frontend .
docker run -d -p 3000:80 --name eng-ai-frontend eng-ai-frontend

# 方式B: 本地开发方式（见下文）
```

### Step 4: 访问应用

打开浏览器访问: **http://localhost:3000**

---

## 方式二：本地开发模式

### 后端启动

```bash
# 终端1: 进入后端目录
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 启动Redis（需要单独安装）
redis-server

# 终端2: 启动Celery Worker
celery -A app.tasks.worker worker --loglevel=info --concurrency=2

# 终端3: 启动FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

```bash
# 终端4: 进入前端目录
cd frontend-web

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问 http://localhost:3000
```

---

## 📝 使用流程

### 1. 用户注册/登录

由于后端认证接口尚未实现（代码中有TODO标记），当前前端使用模拟登录：

**测试账号**（任意输入即可）:
- 用户名: `testuser`
- 密码: `123456`

点击"登录"即可进入系统。

### 2. 上传文档

1. 点击侧边栏"文档上传"
2. 拖拽或选择PDF/DOCX/TXT文件
3. 系统自动上传并开始处理
4. 显示处理进度

### 3. 智能问答

1. 点击侧边栏"智能问答"
2. 输入问题，例如："C30混凝土的配合比是什么？"
3. 按Ctrl+Enter或点击"发送"
4. 查看AI回答和引用来源

### 4. 生成报告

1. 点击侧边栏"报告生成"
2. 选择报告类型（如"混凝土配合比设计"）
3. 填写参数（强度等级、坍落度等）
4. 点击"生成报告"
5. 预览报告内容，可复制或下载

---

## 🔧 故障排查

### 问题1: 前端无法连接后端

**症状**: API请求失败，网络错误

**解决**:
```bash
# 检查后端是否启动
curl http://localhost:8000/health

# 检查前端代理配置
cat frontend-web/.env.development
# 应该包含: VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 问题2: 后端服务未启动

**症状**: 所有API调用返回502或连接错误

**解决**:
```bash
# 检查Docker容器
docker ps | grep eng-ai

# 如果没有运行，启动后端
cd backend
docker-compose up -d
```

### 问题3: npm install失败

**症状**: 依赖安装超时或报错

**解决**:
```bash
# 使用国内镜像
npm config set registry https://registry.npmmirror.com

# 重新安装
npm install
```

### 问题4: 端口被占用

**症状**: EADDRINUSE错误

**解决**:
```bash
# 查看占用端口的进程
lsof -i :3000  # 前端
lsof -i :8000  # 后端

# 停止相关进程或修改端口
```

---

## 🎯 核心功能验证清单

启动系统后，验证以下功能：

- [ ] 能够访问 http://localhost:3000
- [ ] 能够登录（使用任意账号密码）
- [ ] 能够看到首页功能卡片
- [ ] 能够进入文档上传页面
- [ ] 能够进入智能问答页面
- [ ] 能够进入报告生成页面
- [ ] 侧边栏导航正常工作
- [ ] 移动端响应式适配正常

---

## 📊 系统架构概览

```
┌─────────────┐
│   Browser   │
│ localhost:3000 │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Frontend   │  Vue 3 + Element Plus
│  (Port 3000)│
└──────┬──────┘
       │ API Calls
       ↓
┌─────────────┐
│   Backend   │  FastAPI
│  (Port 8000)│
└──────┬──────┘
       │
       ├→ Redis (消息队列)
       ├→ Celery Worker (异步任务)
       └→ ChromaDB (向量数据库)
```

---

## 💡 提示

1. **开发模式**: 前端会自动热重载，后端使用`--reload`也会自动重启
2. **API文档**: 访问 http://localhost:8000/docs 查看后端API
3. **日志查看**: 
   ```bash
   # 前端日志
   npm run dev
   
   # 后端日志
   docker-compose logs -f backend
   docker-compose logs -f celery-worker
   ```

4. **停止服务**:
   ```bash
   # Docker方式
   docker-compose down
   
   # 本地方式
   # Ctrl+C 停止各个进程
   ```

---

## 🎉 开始使用

一切准备就绪！现在您可以：

1. 浏览各个功能页面
2. 尝试上传文档（需要后端完整配置）
3. 体验智能问答
4. 生成工程报告

**祝您使用愉快！** 🚀
