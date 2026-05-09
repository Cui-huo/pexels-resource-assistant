"""
config.py - 配置文件

Author: 仗剑天涯
Date:2026/4/19

说明：
    所有敏感配置优先从环境变量或 .env 文件读取。
    如果没有配置环境变量，则使用下方的默认占位值（需要用户自行替换）。
    
    使用步骤：
    1. 复制 .env.example 为 .env
    2. 在 .env 文件中填入真实的 API Key 和邮箱信息
    3. 运行程序时会自动读取配置

示例用法：
    # 方式 1：直接导入配置常量（适用于开发环境）
    from config import PEXELS_API_KEY, EMAIL_SENDER
    
    # 方式 2：使用初始化函数（推荐，兼容打包后的 exe）
    from config import init_config
    config = init_config()
    print(config['PEXELS_API_KEY'])
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def get_project_root() -> Path:
    """
    获取项目根目录路径，兼容开发环境和打包后的 exe 环境。
    
    Returns:
        项目根目录的 Path 对象
    """
    if getattr(sys, 'frozen', False):
        # 打包后环境：使用 exe 所在目录作为项目根目录
        return Path(sys.executable).parent
    else:
        # 开发环境：使用当前脚本所在目录的父目录作为项目根目录
        return Path(__file__).parent.parent


def init_config():
    """
    初始化配置，加载 .env 文件并返回配置字典。
    
    此函数会自动处理开发环境和打包后环境的路径差异，
    推荐在所有脚本中使用此函数来加载配置。
    
    Returns:
        包含所有配置的字典
    """
    # 获取项目根目录
    project_root = get_project_root()
    
    # 加载项目根目录下的 .env 文件
    env_path = project_root / '.env'
    load_dotenv(dotenv_path=env_path, verbose=False)
    
    # 返回配置字典
    return {
        'PEXELS_API_KEY': os.getenv("PEXELS_API_KEY", "YOUR_PEXELS_API_KEY_HERE"),
        'EMAIL_SENDER': os.getenv("EMAIL_SENDER", "your_email@163.com"),
        'EMAIL_PASSWORD': os.getenv("EMAIL_PASSWORD", "YOUR_EMAIL_AUTH_CODE_HERE"),
        'SMTP_SERVER': os.getenv("SMTP_SERVER", "smtp.163.com"),
        'SMTP_PORT': int(os.getenv("SMTP_PORT", "465")),
        'DEFAULT_RECEIVER': os.getenv("DEFAULT_RECEIVER", "receiver@example.com"),
    }


# ========== 便捷访问函数 ==========

def get_pexels_api_key() -> str:
    """获取 Pexels API Key"""
    return os.getenv("PEXELS_API_KEY", "YOUR_PEXELS_API_KEY_HERE")


def get_email_config() -> dict:
    """获取邮箱配置字典"""
    return {
        'sender': os.getenv("EMAIL_SENDER", "your_email@163.com"),
        'password': os.getenv("EMAIL_PASSWORD", "YOUR_EMAIL_AUTH_CODE_HERE"),
        'smtp_server': os.getenv("SMTP_SERVER", "smtp.163.com"),
        'smtp_port': int(os.getenv("SMTP_PORT", "465")),
        'default_receiver': os.getenv("DEFAULT_RECEIVER", "receiver@example.com"),
    }


def get_download_dir() -> Path:
    """
    获取下载目录路径，确保目录存在。
    
    Returns:
        下载目录的 Path 对象
    """
    project_root = get_project_root()
    download_dir = project_root / 'download_and_send' / 'downloads'
    download_dir.mkdir(parents=True, exist_ok=True)
    return download_dir


# ========== 直接导出的常量（仅开发环境兼容） ==========
# 注意：这些常量在打包后可能无法正确加载，建议在 exe 中使用 init_config() 函数

# 先加载环境变量
_project_root = get_project_root()
load_dotenv(dotenv_path=_project_root / '.env', verbose=False)

# 从环境变量读取，如果没有则使用默认占位值（需要用户替换）
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "YOUR_PEXELS_API_KEY_HERE")
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your_email@163.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "YOUR_EMAIL_AUTH_CODE_HERE")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.163.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
DEFAULT_RECEIVER = os.getenv("DEFAULT_RECEIVER", "receiver@example.com")

# 本地保存目录
DOWNLOAD_DIR = "downloads"
