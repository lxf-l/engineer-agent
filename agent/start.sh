#!/bin/bash
# Engineering AI Agent Backend 快速启动脚本（Linux/Mac）

echo "🚀 Engineering AI Agent Backend 启动中..."

# 检查.env文件
if [ ! -f .env ]; then
    echo "❌ .env文件不存在，正在创建..."
    cp .env.example .env
    echo "⚠️  请编辑.env文件，配置DEEPSEEK_API_KEY和API_KEY"
    exit 1
fi

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

echo "✅ 环境检查通过"
echo "📦 启动Docker容器..."

# 使用docker-compose启动所有服务
docker-compose up -d

echo "⏳ 等待服务启动..."
sleep 5

# 检查容器状态
echo ""
echo "📊 容器状态:"
docker-compose ps

echo ""
echo "✅ 服务启动完成！"
echo ""
echo "📝 访问以下地址:"
echo "   - API文档: http://localhost:8000/docs"
echo "   - 健康检查: http://localhost:8000/health"
echo ""
echo "🔍 查看日志:"
echo "   docker-compose logs -f backend"
echo "   docker-compose logs -f celery-worker"
echo "   docker-compose logs -f redis"
echo ""
echo "🛑 停止服务:"
echo "   docker-compose down"
