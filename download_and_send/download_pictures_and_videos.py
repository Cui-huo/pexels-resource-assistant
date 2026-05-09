"""
download_pictures_and_videos - 

Author:仗剑天涯
Date:2026/4/19
"""
"""
pexels_utils.py - Pexels 图片和视频下载功能
包含获取热门/搜索、下载、交互菜单等
"""

import requests
from pathlib import Path
from config import PEXELS_API_KEY

# ------------------ 通用请求头 ------------------
HEADERS = {"Authorization": PEXELS_API_KEY}

# ================== 图片相关 ==================
def get_popular_photos(per_page: int = 10) -> list:
    """获取 Pexels 热门图片"""
    url = "https://api.pexels.com/v1/curated"
    try:
        resp = requests.get(url, headers=HEADERS, params={"per_page": per_page}, timeout=15)
        resp.raise_for_status()
        return resp.json().get("photos", [])
    except Exception as e:
        print(f"❌ 获取热门图片失败: {e}")
        return []

def search_photos(query: str, per_page: int = 10) -> list:
    """关键词搜索图片"""
    url = "https://api.pexels.com/v1/search"
    try:
        resp = requests.get(url, headers=HEADERS, params={"query": query, "per_page": per_page}, timeout=15)
        resp.raise_for_status()
        return resp.json().get("photos", [])
    except Exception as e:
        print(f"❌ 图片搜索失败: {e}")
        return []

def download_photo(photo_info: dict, save_dir: Path) -> Path | None:
    """下载单张图片，返回保存路径"""
    src = photo_info.get("src", {})
    img_url = src.get("original") or src.get("large2x") or src.get("large")
    if not img_url:
        return None
    ext = ".jpg" if ".jpg" in img_url.lower() else ".png"
    photo_id = photo_info.get("id", "unknown")
    filename = f"pexels_photo_{photo_id}{ext}"
    save_path = save_dir / filename
    try:
        img_resp = requests.get(img_url, timeout=20)
        img_resp.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(img_resp.content)
        print(f"✅ 图片已保存: {save_path.name}")
        return save_path
    except Exception as e:
        print(f"❌ 图片下载失败: {e}")
        return None

def download_photos_interactive(save_dir: Path) -> list[Path]:
    """交互式图片下载菜单，返回下载成功的文件路径列表"""
    print("\n📸 图片下载配置：")
    print("1. 获取热门图片")
    print("2. 关键词搜索图片")
    choice = input("请选择 (1/2): ").strip()

    if choice == "1":
        count = int(input("请输入要下载的图片数量: ").strip())
        photos = get_popular_photos(per_page=count * 2)
    elif choice == "2":
        query = input("请输入搜索关键词 (中英文均可): ").strip()
        count = int(input("请输入要下载的图片数量: ").strip())
        photos = search_photos(query, per_page=count * 2)
    else:
        print("❌ 无效选择，跳过图片下载。")
        return []

    save_dir.mkdir(parents=True, exist_ok=True)
    downloaded = []
    for photo in photos:
        if len(downloaded) >= count:
            break
        path = download_photo(photo, save_dir)
        if path:
            downloaded.append(path)
    print(f"✅ 成功下载 {len(downloaded)} 张图片")
    return downloaded

# ================== 视频相关 ==================
def get_popular_videos(per_page: int = 10) -> list:
    """获取 Pexels 热门视频"""
    url = "https://api.pexels.com/v1/videos/popular"
    try:
        resp = requests.get(url, headers=HEADERS, params={"per_page": per_page}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("videos", [])
    except Exception as e:
        print(f"❌ 获取热门视频失败: {e}")
        return []

def search_videos(query: str, per_page: int = 10) -> list:
    """关键词搜索视频"""
    url = "https://api.pexels.com/v1/videos/search"
    try:
        resp = requests.get(url, headers=HEADERS, params={"query": query, "per_page": per_page}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("videos", [])
    except Exception as e:
        print(f"❌ 视频搜索失败: {e}")
        return []

def select_video_file(video_info: dict) -> dict | None:
    """选择分辨率最小的视频文件（下载更快）"""
    video_files = video_info.get("video_files", [])
    if not video_files:
        return None
    sorted_files = sorted(video_files, key=lambda x: x.get("width", 0))
    return sorted_files[0] if sorted_files else None

def download_video(video_info: dict, save_dir: Path) -> Path | None:
    """下载单个视频，返回保存路径"""
    best_file = select_video_file(video_info)
    if not best_file:
        return None
    video_url = best_file.get("link")
    if not video_url:
        return None
    video_id = video_info.get("id", "unknown")
    photographer = video_info.get("user", {}).get("name", "pexels")
    photographer = "".join(c for c in photographer if c.isalnum() or c in " _-")
    filename = f"pexels_video_{video_id}_{photographer}.mp4"
    save_path = save_dir / filename
    try:
        resp = requests.get(video_url, stream=True, timeout=60)
        resp.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"✅ 视频已保存: {save_path.name}")
        return save_path
    except Exception as e:
        print(f"❌ 视频下载失败: {e}")
        return None

def download_videos_interactive(save_dir: Path) -> list[Path]:
    """交互式视频下载菜单，返回下载成功的文件路径列表"""
    print("\n🎬 视频下载配置：")
    print("1. 获取热门视频")
    print("2. 关键词搜索视频")
    choice = input("请选择 (1/2): ").strip()

    if choice == "1":
        count = int(input("请输入要下载的视频数量: ").strip())
        videos = get_popular_videos(per_page=count * 2)
    elif choice == "2":
        query = input("请输入搜索关键词 (中英文均可): ").strip()
        count = int(input("请输入要下载的视频数量: ").strip())
        videos = search_videos(query, per_page=count * 2)
    else:
        print("❌ 无效选择，跳过视频下载。")
        return []

    save_dir.mkdir(parents=True, exist_ok=True)
    downloaded = []
    for video in videos:
        if len(downloaded) >= count:
            break
        path = download_video(video, save_dir)
        if path:
            downloaded.append(path)
    print(f"✅ 成功下载 {len(downloaded)} 个视频")
    return downloaded


def list_downloaded_files(download_dir: Path) -> list[Path]:
    """返回下载目录中所有文件（图片和视频）的路径列表"""
    if not download_dir.exists():
        return []
    files = list(download_dir.glob("*"))
    # 过滤只保留常见的图片和视频格式
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mov", ".avi"}
    return [f for f in files if f.is_file() and f.suffix.lower() in allowed_extensions]