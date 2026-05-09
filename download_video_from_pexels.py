"""
download_video_from_pexels - 
从pexels上下载热门视频、关键词搜索视频

功能：从 Pexels 平台自动下载热门视频到本地项目文件夹

使用方法：
1. 将 YOUR_PEXELS_API_KEY 替换为你自己的 Pexels API 密钥
2. 运行脚本，第一个热门视频将被下载到当前目录下的 videos 文件夹中

Author:仗剑天涯
Date:2026/4/19
"""

import os
from pprint import pprint

import requests
from pathlib import Path


# ==================== 配置区域 ====================
# 请在此处填入你的 Pexels API 密钥
# 获取方式：登录 Pexels 官网 -> API 页面 -> 申请/查看 API Key
PEXELS_API_KEY = "gH0PMN2NOO6vJuLGK6x3WhKa5H2As3ww9wr5ovGhxLrS0efspR6NmuHv"

# 视频保存目录（默认为当前脚本所在目录下的 videos 文件夹）
SAVE_DIR = Path(__file__).parent / "videos"
# =================================================

def get_videos(url, search_query, api_key: str, per_page: int = 10) -> list:
    """
    调用 Pexels API 获取热门视频列表。

    Pexels 的 videos_popular 端点：GET /v1/videos/popular
    官方文档：https://www.pexels.com/api/documentation/#videos-popular

    Args:
        api_key: Pexels API 密钥
        per_page: 每页返回的视频数量，最大 80，默认 10

    Returns:
        视频信息列表，每个元素为包含视频详情（id、url、video_files 等）的字典
    """
    headers = {"Authorization": api_key}
    params2 = {"per_page": per_page, "query": search_query}
    params = {"per_page": per_page}
    if search_query:
        params = params2

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()  # 如果状态码不是 200，抛出 HTTPError
        data = response.json()
        return data.get("videos", [])
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取热门视频失败: {e}")
        return []


def download_video(video_url: str, save_path: Path) -> bool:
    """
    下载视频文件到本地指定路径。

    Args:
        video_url: 视频文件的直链 URL
        save_path: 保存的本地路径（Path 对象）

    Returns:
        下载成功返回 True，否则返回 False
    """
    try:
        # 发送 GET 请求，stream=True 以流式方式读取，避免一次性加载整个视频到内存
        response = requests.get(video_url, stream=True, timeout=60)
        response.raise_for_status()

        # 以二进制写入模式保存文件
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"✅ 视频已保存: {save_path.name}")
        return True

    except Exception as e:
        print(f"❌ 下载失败 {video_url}: {e}")
        return False


def select_video_file(video_info: dict) -> dict | None:
    """
    从视频信息中选取质量最高的视频文件（优先选择 1920x1080 或更高分辨率）。

    视频的 video_files 字段包含多个不同分辨率的文件链接，
    通常包括 sd、hd、full_hd 等版本，这里优先选择 full_hd。

    Args:
        video_info: Pexels API 返回的单个视频信息字典

    Returns:
        选中的 video_file 字典，包含 link、width、height、quality 等信息；
        如果没有合适的视频文件，返回 None
    """
    video_files = video_info.get("video_files", [])
    if not video_files:
        return None

    # 按分辨率降序排序，优先选择最高清版本
    # width 字段表示视频宽度，越高越清晰
    sorted_files = sorted(
        video_files,
        key=lambda x: x.get("width", 0),
        reverse=False
    )
    return sorted_files[0] if sorted_files else None


def main():
    while True:
        search_query = ''
        # API访问接口
        url = "https://api.pexels.com/v1/videos/popular"
        url2 = "https://api.pexels.com/v1/videos/search"
        # 实现自己选择可用功能
        num = int(input('1、获取热门视频\n2、关键词搜索视频\n请选择功能（数据均从pexels上获取）：'))

        # 下载视频的数量（建议设为 1，避免一次下载过多）
        download_count = int(input('下载视频数：'))
        if num == 2:
            url = url2
            # 搜索关键词
            search_query = input('请输入搜索关键词(中英文均可)：')
        """主函数：获取热门视频并下载到本地"""
        # 1. 检查 API 密钥是否已配置
        if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY":
            print("⚠️ 请先在代码中填入你的 Pexels API 密钥（替换 YOUR_PEXELS_API_KEY）")
            print("获取方式：登录 https://www.pexels.com/api/ 申请")
            return

        # 2. 创建保存目录（如果不存在）
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        print(f"📁 视频将保存至: {SAVE_DIR.absolute()}")

        # 3. 获取热门视频列表
        print("🔍 正在获取 Pexels 热门视频...")
        videos = get_videos(url, search_query, PEXELS_API_KEY,
             per_page=10 if download_count * 2 < 5 else download_count * 2)
        if not videos:
            print("❌ 未获取到任何视频，请检查 API 密钥是否正确或稍后重试。")
            return

        # 4. 下载指定数量的视频
        downloaded = 0
        for i, video in enumerate(videos):
            if downloaded >= download_count:
                break

            # 获取视频 ID 和拍摄者信息，用于命名文件
            video_id = video.get("id", "unknown")
            photographer = video.get("user", {}).get("name", "pexels")
            # 清理文件名中的非法字符
            photographer = "".join(c for c in photographer if c.isalnum() or c in " _-")

            # 选择最小的视频文件
            min_video = select_video_file(video)
            if not min_video:
                print(f"⚠️ 视频 {video_id} 没有可用的视频文件链接，跳过。")
                continue

            video_url = min_video.get("link")
            if not video_url:
                print(f"⚠️ 视频 {video_id} 的视频链接无效，跳过。")
                continue

            # 构造文件名：pexels_video_{id}_{photographer}.mp4
            filename = f"pexels_video_{video_id}_{photographer}.mp4"
            save_path = SAVE_DIR / filename

            if download_video(video_url, save_path):
                downloaded += 1

        print(f"\n🎉 完成！共成功下载 {downloaded} 个视频到 {SAVE_DIR.absolute()}")


if __name__ == "__main__":
    main()