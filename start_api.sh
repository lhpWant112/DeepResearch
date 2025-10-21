#!/bin/bash

# React Agent API Server 启动脚本

# 设置环境变量
export MODEL_NAME=${MODEL_NAME:-"qwen-plus"}
export MAX_RETRIES=${MAX_RETRIES:-10}
export TEMPERATURE=${TEMPERATURE:-0.6}
export TOP_P=${TOP_P:-0.95}
export PRESENCE_PENALTY=${PRESENCE_PENALTY:-1.1}
export MODEL_TYPE=${MODEL_TYPE:-"qwen_dashscope"}

# 检查是否安装了必要的依赖
echo "Checking dependencies..."
if ! command -v python &> /dev/null
then
    echo "Python is not installed. Please install Python first."
    exit 1
fi

# 检查 FastAPI 是否安装
if ! python -c "import fastapi" &> /dev/null
then
    echo "FastAPI is not installed. Installing..."
    pip install fastapi uvicorn
fi

# 启动服务
echo "Starting React Agent API server..."
echo "Model: $MODEL_NAME"
echo "Host: 0.0.0.0"
echo "Port: 8000"

python inference/api_server.py --host 0.0.0.0 --port 8000