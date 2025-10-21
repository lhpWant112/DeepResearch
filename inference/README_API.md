# React Agent API Server

这是一个将 `react_agent.py` 以 RESTful API 服务形式暴露的 FastAPI 应用，供其他系统调用。

## 功能特性

- 提供 RESTful API 接口来调用 React Agent
- 支持跨域请求 (CORS)
- 完善的错误处理和日志记录
- 健康检查接口
- 可配置的环境变量

## 启动服务

### 方法 1: 使用启动脚本 (推荐)

```bash
./start_api.sh
```

### 方法 2: 直接运行 Python 脚本

```bash
python inference/api_server.py
```

默认情况下，服务会在 `0.0.0.0:8000` 上启动。

### 配置参数

可以通过命令行参数或环境变量来配置服务：

```bash
# 命令行参数
python inference/api_server.py --host 0.0.0.0 --port 8000

# 环境变量
export MODEL_NAME="qwen-plus"
export MAX_RETRIES=10
export TEMPERATURE=0.6
export TOP_P=0.95
export PRESENCE_PENALTY=1.1
export MODEL_TYPE="qwen_dashscope"
```

## API 接口

### 1. 运行 Agent

**POST** `/agent/run`

请求体:
```json
{
  "item": {
    "question": "你的问题",
    "answer": "答案(可选)"
  },
  "planning_port": 6001,
  "model": "模型名称"
}
```

响应:
```json
{
  "question": "问题",
  "answer": "答案",
  "messages": [],
  "prediction": "预测结果",
  "termination": "终止原因"
}
```

### 2. 健康检查

**GET** `/health`

响应:
```json
{
  "status": "healthy",
  "agent_initialized": true
}
```

### 3. 根路径

**GET** `/`

返回 API 信息和可用端点。

## 测试

可以使用以下脚本测试服务:

```bash
# 测试服务是否正常运行
./test_api.sh

# 或者使用 Python 客户端测试
python test_api_client.py
```

## 依赖

- Python 3.7+
- FastAPI
- Uvicorn
- 其他项目依赖 (见 requirements.txt)

安装依赖:
```bash
pip install -r requirements.txt
pip install fastapi uvicorn
```