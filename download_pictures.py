"""
download_woman_images.py - 从 Pexels 下载女性主题的高清图片

Author: 仗剑天涯
Date: 2026/4/18
Description:
    使用 Pexels 官方 API 搜索并下载指定数量的女性图片到桌面。
    需要提供有效的 Pexels API Key。
"""

import os
import requests
from pathlib import Path

# ==================== 配置区域 ====================
API_KEY = "gH0PMN2NOO6vJuLGK6x3WhKa5H2As3ww9wr5ovGhxLrS0efspR6NmuHv"  # 你的 Pexels API 密钥
QUERY = "woman"          # 搜索关键词
COUNT = 2                # 需要下载的图片数量
# =================================================


def search_pexels_images(query: str, per_page: int = 10) -> list:
    """
    使用 Pexels API 搜索图片。

    Args:
        query: 搜索关键词
        per_page: 每页返回的图片数量（默认10，最大80）

    Returns:
        包含图片信息的列表，每个元素为 dict
    """
    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": API_KEY  # API 认证头
    }
    params = {
        "query": query,
        "per_page": per_page
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()  # 如果状态码不是 200，抛出异常
        data = response.json()
        return data.get("photos", [])
    except requests.exceptions.RequestException as e:
        print(f"❌ API 请求失败: {e}")
        return []


def download_image(image_url: str, save_path: Path) -> bool:
    """
    下载单张图片并保存到指定路径。

    Args:
        image_url: 图片的 URL 地址
        save_path: 保存的本地路径（Path 对象）

    Returns:
        下载成功返回 True，否则返回 False
    """
    try:
        # 发送 GET 请求下载图片内容
        img_response = requests.get(image_url, timeout=20)
        img_response.raise_for_status()

        # 以二进制写入文件
        with open(save_path, "wb") as f:
            f.write(img_response.content)

        print(f"✅ 已保存: {save_path.name}")
        return True

    except Exception as e:
        print(f"❌ 下载失败 {image_url}: {e}")
        return False


def main():
    """主函数：搜索图片并下载到桌面"""
    # 1. 确定桌面路径（兼容 Windows / macOS / Linux）
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        # 如果系统是中文版 Windows，桌面可能在 "桌面" 文件夹下
        desktop = Path.home() / "桌面"
    if not desktop.exists():
        print("❌ 无法定位桌面路径，请手动指定保存目录。")
        return

    print(f"🔍 正在 Pexels 搜索关键词 '{QUERY}' ...")
    photos = search_pexels_images(QUERY, per_page=COUNT * 2)  # 多搜一些，以防有的图片无效

    if not photos:
        print("❌ 未搜索到任何图片，请检查网络或 API 密钥是否有效。")
        return

    # 2. 下载前 COUNT 张有效图片
    downloaded = 0
    for i, photo in enumerate(photos):
        if downloaded >= COUNT:
            break

        # Pexels 返回的图片 URL 有多种尺寸，优先选择高质量的原图或大图
        src_info = photo.get("src", {})
        img_url = src_info.get("original") or src_info.get("large2x") or src_info.get("large")

        if not img_url:
            print(f"⚠️ 第 {i+1} 张图片缺少有效 URL，跳过。")
            continue

        # 根据 URL 推断文件扩展名
        ext = ".jpg"  # Pexels 图片多为 jpg
        if ".png" in img_url.lower():
            ext = ".png"

        filename = f"pexels_{QUERY}_{downloaded+1:02d}{ext}"
        save_path = desktop / filename

        if download_image(img_url, save_path):
            downloaded += 1

    print(f"\n🎉 完成！共成功下载 {downloaded} 张图片到桌面：{desktop}")


if __name__ == "__main__":
    main()