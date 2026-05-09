"""
utils/config_helper.py - 配置导入辅助模块

提供统一的配置导入函数，兼容开发环境和打包后的 exe 环境。

使用方法：
    from utils.config_helper import get_config
    config = get_config()
    print(config['PEXELS_API_KEY'])
    
或者直接使用便捷函数：
    from utils.config_helper import get_pexels_api_key, get_email_config
    api_key = get_pexels_api_key()
    email_cfg = get_email_config()
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
        # 开发环境：使用当前脚本所在目录作为项目根目录
        return Path(__file__).parent.parent


def _load_env():
    """加载 .env 文件到环境变量"""
    project_root = get_project_root()
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, verbose=False)


def get_config():
    """
    获取完整配置字典。
    
    Returns:
        包含所有配置的字典
    """
    _load_env()
    return {
        'PEXELS_API_KEY': os.getenv("PEXELS_API_KEY", "YOUR_PEXELS_API_KEY_HERE"),
        'EMAIL_SENDER': os.getenv("EMAIL_SENDER", "your_email@163.com"),
        'EMAIL_PASSWORD': os.getenv("EMAIL_PASSWORD", "YOUR_EMAIL_AUTH_CODE_HERE"),
        'SMTP_SERVER': os.getenv("SMTP_SERVER", "smtp.163.com"),
        'SMTP_PORT': int(os.getenv("SMTP_PORT", "465")),
        'DEFAULT_RECEIVER': os.getenv("DEFAULT_RECEIVER", "receiver@example.com"),
    }


def get_pexels_api_key() -> str:
    """获取 Pexels API Key"""
    _load_env()
    return os.getenv("PEXELS_API_KEY", "YOUR_PEXELS_API_KEY_HERE")


def get_email_config() -> dict:
    """
    获取邮箱配置字典
    
    Returns:
        {
            'sender': str,      # 发件人邮箱
            'password': str,    # SMTP 授权码
            'smtp_server': str, # SMTP 服务器
            'smtp_port': int,   # SMTP 端口
            'default_receiver': str  # 默认收件人
        }
    """
    _load_env()
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


def get_output_dir(sub_dir: str = "output") -> Path:
    """
    获取输出目录路径，确保目录存在。
    
    Args:
        sub_dir: 子目录名称
        
    Returns:
        输出目录的 Path 对象
    """
    project_root = get_project_root()
    output_dir = project_root / sub_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


# 预加载环境变量（模块导入时自动执行）
_load_env()
