import requests
import json
import time

# 测试数据
test_data = {
    "item": {
        "question": "What is the capital of France?",
        "answer": "Paris"
    },
    "planning_port": 6001,
    "model": "qwen-plus"
}

def test_api():
    base_url = "http://localhost:8000"
    
    # 测试根路径
    print("Testing root endpoint...")
    response = requests.get(f"{base_url}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("")
    
    # 测试健康检查
    print("Testing health check endpoint...")
    response = requests.get(f"{base_url}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("")
    
    # 测试 agent/run 接口
    print("Testing agent/run endpoint...")
    try:
        response = requests.post(
            f"{base_url}/agent/run",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Exception occurred: {e}")
    print("")

if __name__ == "__main__":
    test_api()