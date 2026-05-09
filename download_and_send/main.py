"""
main.py - 主程序入口
主菜单：
  1. 下载和搜索图片
  2. 下载和搜索视频
  3. 发送本地文件到邮箱
"""
# ================== 路径处理（必须放在所有导入之前） ==================
import sys
import os
from config import DOWNLOAD_DIR
# 确保程序在打包后，能够找到和 main.exe 放在同一目录下的 config.py、download_pictures_and_videos.py 等模块。
if getattr(sys, 'frozen', False):
    # 如果是打包后的 exe 运行，将 exe 所在目录添加到模块搜索路径
    exe_dir = os.path.dirname(sys.executable)
    if exe_dir not in sys.path:
        sys.path.insert(0, exe_dir)
# ====================================================================


from pathlib import Path
from config import DOWNLOAD_DIR, DEFAULT_RECEIVER
from download_pictures_and_videos import (
    get_popular_photos, search_photos, download_photo,
    get_popular_videos, search_videos, download_video,
    list_downloaded_files
)
from send_email import send_email


def menu_send_local_files():
    """发送本地任意文件到邮箱（不限于已下载的 Pexels 资源）"""
    print("\n📎 发送本地文件")
    print("💡 提示：可以直接将文件拖拽到本窗口，自动填入路径")
    print("   输入多个文件路径时，用英文逗号分隔")

    # 获取用户输入的文件路径
    paths_input = input("请输入文件路径（多个用逗号分隔）: ").strip()
    if not paths_input:
        print("❌ 未输入任何路径，取消发送。")
        return

    # 解析路径
    raw_paths = [p.strip().strip('"') for p in paths_input.split(",")]  # 去除引号（拖拽文件时可能带有）
    file_paths = []
    for rp in raw_paths:
        p = Path(rp)
        if p.exists() and p.is_file():
            file_paths.append(p)
        else:
            print(f"⚠️ 文件不存在或不是有效文件，已跳过: {rp}")

    if not file_paths:
        print("❌ 没有有效的文件，取消发送。")
        return

    # 显示选中的文件
    print("\n📋 将发送以下文件：")
    for i, f in enumerate(file_paths, 1):
        size_kb = f.stat().st_size / 1024
        print(f"  {i}. {f.name} ({size_kb:.1f} KB)")

    # 收件人邮箱
    print(f"\n📧 收件人邮箱 (直接回车使用默认 {DEFAULT_RECEIVER}):")
    receiver = input("请输入: ").strip()
    if not receiver:
        receiver = DEFAULT_RECEIVER

    # 发送
    subject = f"本地文件推送 - 共 {len(file_paths)} 个文件"
    body = "您好！\n\n以下是您选择的本地文件，请查收附件。"
    send_email(subject, body, file_paths, receiver=receiver)


def menu_photos(download_dir: Path):
    """图片下载子菜单"""
    while True:
        print("\n" + "=" * 40)
        print("📸 图片下载子菜单")
        print("1. 关键词搜索图片")
        print("2. 直接下载热门图片")
        print("3. 回到主菜单")
        choice = input("请选择 (1/2/3): ").strip()

        if choice == "1":
            query = input("请输入搜索关键词: ").strip()
            if not query:
                print("❌ 关键词不能为空")
                continue
            try:
                count = int(input("请输入要下载的图片数量: ").strip())
            except ValueError:
                print("❌ 数量必须是数字")
                continue
            photos = search_photos(query, per_page=count * 2)
        elif choice == "2":
            try:
                count = int(input("请输入要下载的图片数量: ").strip())
            except ValueError:
                print("❌ 数量必须是数字")
                continue
            photos = get_popular_photos(per_page=count * 2)
        elif choice == "3":
            break
        else:
            print("❌ 无效选择，请重新输入")
            continue

        download_dir.mkdir(parents=True, exist_ok=True)
        downloaded = 0
        for photo in photos:
            if downloaded >= count:
                break
            path = download_photo(photo, download_dir)
            if path:
                downloaded += 1
        print(f"✅ 本次成功下载 {downloaded} 张图片")

def menu_videos(download_dir: Path):
    """视频下载子菜单"""
    while True:
        print("\n" + "=" * 40)
        print("🎬 视频下载子菜单")
        print("1. 关键词搜索视频")
        print("2. 直接下载热门视频")
        print("3. 回到主菜单")
        choice = input("请选择 (1/2/3): ").strip()

        if choice == "1":
            query = input("请输入搜索关键词: ").strip()
            if not query:
                print("❌ 关键词不能为空")
                continue
            try:
                count = int(input("请输入要下载的视频数量: ").strip())
            except ValueError:
                print("❌ 数量必须是数字")
                continue
            videos = search_videos(query, per_page=count * 2)
        elif choice == "2":
            try:
                count = int(input("请输入要下载的视频数量: ").strip())
            except ValueError:
                print("❌ 数量必须是数字")
                continue
            videos = get_popular_videos(per_page=count * 2)
        elif choice == "3":
            break
        else:
            print("❌ 无效选择，请重新输入")
            continue

        download_dir.mkdir(parents=True, exist_ok=True)
        downloaded = 0
        for video in videos:
            if downloaded >= count:
                break
            path = download_video(video, download_dir)
            if path:
                downloaded += 1
        print(f"✅ 本次成功下载 {downloaded} 个视频")

def menu_send_email(download_dir: Path):
    """发送邮件子菜单：列出已下载文件供用户选择"""
    files = list_downloaded_files(download_dir)
    if not files:
        print("\n❌ 下载目录中没有文件，请先下载图片或视频。")
        return

    # 显示文件列表
    print("\n📁 已下载的文件列表：")
    for i, f in enumerate(files, 1):
        size_kb = f.stat().st_size / 1024
        print(f"  {i}. {f.name} ({size_kb:.1f} KB)")

    # 让用户选择文件（支持多选，用逗号分隔）
    print("\n💡 请输入要发送的文件编号（多个编号用逗号分隔，如 1,3,5）")
    print("   直接回车则发送全部文件")
    choice = input("请输入编号: ").strip()

    selected_files = []
    if choice == "":
        selected_files = files
    else:
        try:
            indices = [int(x.strip()) for x in choice.split(",")]
            for idx in indices:
                if 1 <= idx <= len(files):
                    selected_files.append(files[idx - 1])
                else:
                    print(f"⚠️ 编号 {idx} 无效，已跳过")
        except ValueError:
            print("❌ 输入格式错误，操作取消")
            return

    if not selected_files:
        print("❌ 没有选中任何文件")
        return

    # 输入收件人邮箱
    print(f"\n📧 收件人邮箱 (直接回车使用默认 {DEFAULT_RECEIVER}):")
    receiver = input("请输入: ").strip()
    if not receiver:
        receiver = DEFAULT_RECEIVER

    # 邮件主题和正文
    subject = f"Pexels 资源推送 - 共 {len(selected_files)} 个文件"
    body = "您好！\n\n以下是您选择的文件，请查收附件。"
    send_email(subject, body, selected_files, receiver=receiver)


def get_download_dir(base_dir_name: str = DOWNLOAD_DIR) -> Path:
    """
    解决打包后Path(__file__)指向变成了临时目录，无法看到下载文件的问题
    当程序被打包成 exe 时，Python 脚本会被解压到临时目录运行，
    此时 __file__ 指向的是临时目录而非 exe 真实所在文件夹。
    因此必须区分环境，使用不同的基准路径。
    :param base_dir_name:
    :return:
    """
    if getattr(sys, 'frozen', False):
        # 打包后：使用 exe 所在目录作为基准
        # sys.executable是当前 Python 解释器的路径。在打包后，它指向的是生成的
        # .exe 文件的完整路径（例如 C:\Users\仗剑天涯\Desktop\pexels资源助手2.0\main.exe）。
        base_dir = Path(sys.executable).parent

    else:
        # 开发环境：使用脚本所在目录
        base_dir = Path(__file__).parent

    download_dir = base_dir / base_dir_name
    download_dir.mkdir(exist_ok=True)
    return download_dir


def main():
    # 准备下载目录
    download_dir = get_download_dir()

    while True:
        print("\n" + "=" * 50)
        print("   🚀 Pexels 资源助手 - 主菜单")
        print("=" * 50)
        print("1. 下载和搜索图片")
        print("2. 下载和搜索视频")
        print("3. 发送已下载的 Pexels 文件到邮箱")
        print("4. 发送本地任意文件到邮箱")  # 新增
        print("5. 退出程序")
        choice = input("请输入选项 (1/2/3/4/5): ").strip()

        if choice == "1":
            menu_photos(download_dir)
        elif choice == "2":
            menu_videos(download_dir)
        elif choice == "3":
            menu_send_email(download_dir)
        elif choice == "4":
            menu_send_local_files()  # 新增调用
        elif choice == "5":
            print("👋 感谢使用，再见！")
            break
        else:
            print("❌ 无效选项，请重新输入")


if __name__ == "__main__":
    main()