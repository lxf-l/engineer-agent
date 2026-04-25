#!/usr/bin/env python3
"""
Test YAML configuration loading
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.core.config import settings
from app.core.yaml_config import yaml_settings


def test_yaml_config():
    """Test YAML configuration loading"""
    print("Testing YAML configuration...")
    
    if yaml_settings:
        print("✅ YAML配置加载成功!")
        print(f"DeepSeek API Key: {yaml_settings.llm['deepseek']['api_key'][:10]}...")
        print(f"Database URL: {yaml_settings.database['sqlite']['url']}")
        print(f"Upload Directory: {yaml_settings.file_upload.upload_directory}")
    else:
        print("⚠️ YAML配置未找到，使用环境变量配置")
    
    print("\nTesting Pydantic Settings...")
    print(f"DEEPSEEK_API_KEY: {settings.DEEPSEEK_API_KEY[:10]}...")
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(f"UPLOAD_DIR: {settings.UPLOAD_DIR}")


if __name__ == "__main__":
    test_yaml_config()
