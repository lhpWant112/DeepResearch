import argparse
import json
import os
import traceback
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import logging
from react_agent import MultiTurnReactAgent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(title="React Agent API", version="1.0.0")

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局 agent 实例
agent: Optional[MultiTurnReactAgent] = None

class AgentRequest(BaseModel):
    item: Dict[str, Any]
    planning_port: int
    model: str

class AgentResponse(BaseModel):
    question: str
    answer: str
    messages: list
    prediction: str
    termination: str

class ErrorResponse(BaseModel):
    detail: str
    error_type: str

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_type": type(exc).__name__
        }
    )

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化 agent"""
    global agent
    # 默认的 LLM 配置
    llm_cfg = {
        'model': os.getenv('MODEL_NAME', 'qwen-plus'),  # 从环境变量获取模型名
        'generate_cfg': {
            'max_input_tokens': 320000,
            'max_retries': int(os.getenv('MAX_RETRIES', '10')),
            'temperature': float(os.getenv('TEMPERATURE', '0.6')),
            'top_p': float(os.getenv('TOP_P', '0.95')),
            'presence_penalty': float(os.getenv('PRESENCE_PENALTY', '1.1'))
        },
        'model_type': os.getenv('MODEL_TYPE', 'qwen_dashscope')
    }
    
    logger.info("Initializing agent with config: %s", json.dumps(llm_cfg, indent=2))
    
    try:
        agent = MultiTurnReactAgent(
            llm=llm_cfg,
            function_list=["search", "visit", "google_scholar", "PythonInterpreter"]
        )
        logger.info("Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        logger.error(traceback.format_exc())
        raise

@app.post("/agent/run", response_model=AgentResponse, responses={500: {"model": ErrorResponse}})
async def run_agent(request: AgentRequest):
    """运行 agent 处理请求"""
    global agent
    
    if agent is None:
        logger.error("Agent not initialized")
        raise HTTPException(
            status_code=500, 
            detail="Agent not initialized",
            headers={"X-Error-Type": "AgentNotInitialized"}
        )
    
    try:
        logger.info(f"Processing request for question: {request.item.get('question', 'N/A')}")
        logger.debug(f"Request data: {json.dumps(request.dict(), indent=2)}")
        
        # 调用 agent 的 _run 方法
        result = agent._run(
            data=request.dict(),
            model=request.model
        )
        
        logger.info(f"Agent run completed for question: {result.get('question', 'N/A')}")
        logger.debug(f"Result: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, 
            detail=str(e),
            headers={"X-Error-Type": type(e).__name__}
        )

@app.get("/health", responses={200: {"model": Dict[str, Any]}, 500: {"model": ErrorResponse}})
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "agent_initialized": agent is not None}

@app.get("/", responses={200: {"model": Dict[str, Any]}})
async def root():
    """根路径，返回 API 信息"""
    return {
        "message": "React Agent API Server", 
        "version": "1.0.0",
        "endpoints": {
            "/agent/run": "POST - 运行 agent 处理任务",
            "/health": "GET - 健康检查",
            "/": "GET - API 信息"
        }
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    
    logger.info(f"Starting server on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)