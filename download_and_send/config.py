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
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录下的 .env 文件
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# ========== Pexels API 配置 ==========
# 从环境变量读取，如果没有则使用默认占位值（需要用户替换）
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "YOUR_PEXELS_API_KEY_HERE")

# ========== 邮箱配置 ==========
# 从环境变量读取，如果没有则使用默认占位值（需要用户替换）
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your_email@163.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "YOUR_EMAIL_AUTH_CODE_HERE")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.163.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))

# 收件人默认值（运行时可以手动修改）
DEFAULT_RECEIVER = os.getenv("DEFAULT_RECEIVER", "receiver@example.com")

# ========== 本地保存目录 ==========
# 下载的图片和视频会暂时存在这个文件夹里，发送邮件后可以保留或手动删除
DOWNLOAD_DIR = "downloads"
