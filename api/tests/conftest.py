"""
测试配置文件，用于设置pytest环境
"""
import sys
import os
from pathlib import Path

# 确保当前工作目录是api目录
# 这样可以确保测试能够正确导入模块
api_root = Path(__file__).parent.parent
os.chdir(api_root) 