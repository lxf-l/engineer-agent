@echo off
REM Engineering AI Agent Backend 快速启动脚本（Windows）

echo.
echo 🚀 Engineering AI Agent Backend 启动中...
echo.

REM 检查.env文件
if not exist .env (
    echo ❌ .env文件不存在，正在创建...
    copy .env.example .env
    echo ⚠️  请编辑.env文件，配置DEEPSEEK_API_KEY和API_KEY
    pause
    exit /b 1
)

REM 检查Docker是否安装
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker未安装，请先安装Docker
    pause
    exit /b 1
)

REM 检查Docker Compose是否安装
where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker Compose未安装，请先安装Docker Compose
    pause
    exit /b 1
)

echo ✅ 环境检查通过
echo 📦 启动Docker容器...
echo.

REM 使用docker-compose启动所有服务
docker-compose up -d

echo ⏳ 等待服务启动...
timeout /t 5 /nobreak >nul

echo.
echo 📊 容器状态:
docker-compose ps

echo.
echo ✅ 服务启动完成！
echo.
echo 📝 访问以下地址:
echo    - API文档: http://localhost:8000/docs
echo    - 健康检查: http://localhost:8000/health
echo.
echo 🔍 查看日志:
echo    docker-compose logs -f backend
echo    docker-compose logs -f celery-worker
echo    docker-compose logs -f redis
echo.
echo 🛑 停止服务:
echo    docker-compose down
echo.

pause
