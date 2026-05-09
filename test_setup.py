#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速环境测试脚本
使用方法：python test_setup.py
如果所有测试通过，说明环境配置正确，可以正常使用主程序。

环境变量 CI_MODE:
    - 如果在 CI 环境运行（CI_MODE=1），只测试代码导入，不测试配置
    - 本地运行时测试完整配置
"""

import sys
import os

# 检测是否在 CI 环境中运行
CI_MODE = os.getenv('CI_MODE', '0') == '1'

def print_result(name, passed, message=""):
    """打印测试结果"""
    status = "✅" if passed else "❌"
    result = "通过" if passed else "失败"
    print(f"{status} {name}: {result}")
    if message and not passed:
        print(f"   └─ {message}")
    return passed

def main():
    print("=" * 50)
    print("🧪 Pexels 资源助手 - 环境测试")
    if CI_MODE:
        print("           (CI 模式：仅测试代码导入)")
    print("=" * 50)

    all_passed = True

    # 测试 1: Python 版本
    print("\n📌 测试 1: Python 版本")
    python_version = sys.version_info
    passed = python_version.major >= 3 and python_version.minor >= 8
    all_passed &= print_result(
        f"Python {python_version.major}.{python_version.minor}.{python_version.micro}",
        passed,
        "需要 Python 3.8 或更高版本"
    )

    # 测试 2: 依赖包
    print("\n📌 测试 2: 检查依赖包")
    required_packages = ['requests', 'dotenv']
    for pkg in required_packages:
        try:
            if pkg == 'dotenv':
                __import__('dotenv')
            else:
                __import__(pkg)
            all_passed &= print_result(f"{pkg}", True)
        except ImportError as e:
            all_passed &= print_result(f"{pkg}", False, f"请运行：pip install -r requirements.txt")

    # 测试 3: 配置文件（仅本地模式测试）
    if not CI_MODE:
        print("\n📌 测试 3: 检查配置文件")
        env_example_exists = os.path.exists('.env.example')
        all_passed &= print_result(".env.example 存在", env_example_exists)

        env_exists = os.path.exists('.env')
        all_passed &= print_result(".env 文件存在", env_exists, "请复制 .env.example 为 .env 并填写配置")

        # 测试 4: API 配置（如果 .env 存在）
        if env_exists:
            print("\n📌 测试 4: 验证 API 配置")
            from download_and_send.config import PEXELS_API_KEY, EMAIL_SENDER, EMAIL_PASSWORD

            api_configured = PEXELS_API_KEY != "YOUR_PEXELS_API_KEY_HERE"
            all_passed &= print_result("Pexels API Key 已配置", api_configured, "请在 .env 文件中填入有效的 API Key")

            email_configured = EMAIL_SENDER != "your_email@163.com"
            all_passed &= print_result("邮箱账号已配置", email_configured, "请在 .env 文件中填入你的邮箱")

            password_configured = EMAIL_PASSWORD != "YOUR_EMAIL_AUTH_CODE_HERE"
            all_passed &= print_result("邮箱授权码已配置", password_configured, "请在 .env 文件中填入授权码")

            # 测试 5: API 连接（可选）
            if api_configured:
                print("\n📌 测试 5: 测试 Pexels API 连接")
                try:
                    import requests
                    headers = {"Authorization": PEXELS_API_KEY}
                    response = requests.get("https://api.pexels.com/v1/curated?per_page=1",
                                           headers=headers, timeout=10)
                    api_works = response.status_code == 200
                    all_passed &= print_result("Pexels API 连接", api_works,
                                              f"API 返回状态码：{response.status_code}")
                except Exception as e:
                    all_passed &= print_result("Pexels API 连接", False, str(e))
    else:
        # CI 模式：只测试核心模块导入
        print("\n📌 测试 3: 测试核心模块导入 (CI 模式)")
        
        # 添加 download_and_send 到路径
        from pathlib import Path
        dl_dir = Path(__file__).parent / 'download_and_send'
        if str(dl_dir) not in sys.path:
            sys.path.insert(0, str(dl_dir))
        
        try:
            from config import PEXELS_API_KEY
            all_passed &= print_result("config.py 导入", True)
        except Exception as e:
            all_passed &= print_result("config.py 导入", False, str(e))

        try:
            from download_pictures_and_videos import get_popular_photos
            all_passed &= print_result("download_pictures_and_videos.py 导入", True)
        except Exception as e:
            all_passed &= print_result("download_pictures_and_videos.py 导入", False, str(e))

        try:
            from send_email import send_email
            all_passed &= print_result("send_email.py 导入", True)
        except Exception as e:
            all_passed &= print_result("send_email.py 导入", False, str(e))

        print("\n📌 测试 4: 测试独立脚本导入")
        scripts_to_test = [
            'download_pictures',
            'download_video_from_pexels',
            'email_extend',
        ]
        for script in scripts_to_test:
            try:
                __import__(script)
                all_passed &= print_result(f"{script}.py 导入", True)
            except Exception as e:
                all_passed &= print_result(f"{script}.py 导入", False, str(e))

    # 总结
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！")
        if not CI_MODE:
            print("你可以开始使用主程序了。")
            print("\n运行主程序：")
            print("  cd download_and_send")
            print("  python main.py")
    else:
        print("⚠️  部分测试未通过，请先解决上述问题。")
        if not CI_MODE:
            print("\n常见问题解决：")
            print("  1. 安装依赖：pip install -r requirements.txt")
            print("  2. 复制配置：copy .env.example .env")
            print("  3. 编辑 .env 文件，填入你的 API Key 和邮箱信息")
    print("=" * 50)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
