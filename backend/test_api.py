"""
API测试示例脚本
使用前请先确保服务已启动，并修改API_KEY配置
"""
import requests
from pathlib import Path

# 配置
BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "your_app_secret_key"  # 修改为你的API Key

HEADERS = {
    "X-API-Key": API_KEY,
}


def test_health():
    """测试健康检查"""
    print("=" * 50)
    print("测试1: 健康检查")
    print("=" * 50)
    
    response = requests.get("http://localhost:8000/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}\n")


def test_upload_document(file_path: str):
    """测试文档上传"""
    print("=" * 50)
    print("测试2: 上传文档")
    print("=" * 50)
    
    with open(file_path, 'rb') as f:
        files = {'file': (Path(file_path).name, f)}
        response = requests.post(
            f"{BASE_URL}/upload/",
            headers=HEADERS,
            files=files
        )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {result}\n")
    
    return result.get('task_id')


def test_task_status(task_id: str):
    """测试任务状态查询"""
    print("=" * 50)
    print("测试3: 查询任务状态")
    print("=" * 50)
    
    response = requests.get(
        f"{BASE_URL}/upload/task/{task_id}",
        headers=HEADERS
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}\n")
    
    return response.json()


def test_rag_query(question: str):
    """测试RAG问答"""
    print("=" * 50)
    print("测试4: RAG问答")
    print("=" * 50)
    
    payload = {
        "question": question,
        "top_k": 5
    }
    
    response = requests.post(
        f"{BASE_URL}/query/",
        headers=HEADERS,
        json=payload
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"答案: {result.get('answer', '')[:200]}...")
    print(f"来源数量: {len(result.get('sources', []))}")
    print(f"处理时间: {result.get('processing_time_ms', 0)}ms\n")


def test_report_generation():
    """测试报告生成"""
    print("=" * 50)
    print("测试5: 生成混凝土配合比报告")
    print("=" * 50)
    
    payload = {
        "report_type": "concrete_mix",
        "parameters": {
            "strength_grade": "C30",
            "slump": "160mm",
            "environment": "室内干燥环境",
            "aggregate_type": "碎石"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/report/",
        headers=HEADERS,
        json=payload
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"报告长度: {len(result.get('content', ''))} 字符")
    print(f"引用规范数: {len(result.get('references', []))}")
    print(f"生成时间: {result.get('generated_at', '')}\n")


if __name__ == "__main__":
    print("\n🚀 Engineering AI Agent API 测试开始\n")
    
    # 1. 健康检查
    try:
        test_health()
    except Exception as e:
        print(f"健康检查失败: {e}\n")
    
    # 2. 文档上传（如果有测试文件）
    test_file = "test_document.pdf"
    task_id = None
    if Path(test_file).exists():
        try:
            task_id = test_upload_document(test_file)
        except Exception as e:
            print(f"文档上传失败: {e}\n")
    else:
        print(f"跳过文档上传测试（未找到 {test_file}）\n")
    
    # 3. 任务状态查询（如果有task_id）
    if task_id:
        try:
            import time
            print("等待5秒后查询任务状态...")
            time.sleep(5)
            test_task_status(task_id)
        except Exception as e:
            print(f"任务状态查询失败: {e}\n")
    
    # 4. RAG问答
    try:
        test_rag_query("C30混凝土的配合比是什么？")
    except Exception as e:
        print(f"RAG问答失败: {e}\n")
    
    # 5. 报告生成
    try:
        test_report_generation()
    except Exception as e:
        print(f"报告生成失败: {e}\n")
    
    print("\n✅ 测试完成")
