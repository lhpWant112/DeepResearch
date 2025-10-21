#!/bin/bash

# 启动 API 服务
echo "Starting React Agent API server..."
python inference/api_server.py --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# 等待服务启动
sleep 5

# 测试健康检查接口
echo "Testing health check endpoint..."
curl -X GET "http://localhost:8000/health" -H "accept: application/json"
echo ""

# 测试根路径接口
echo "Testing root endpoint..."
curl -X GET "http://localhost:8000/" -H "accept: application/json"
echo ""

# 关闭服务
kill $SERVER_PID
echo "Server stopped."