"""
send_email_pictures_from_pexels -
实现功能：
从 pexels 中下载 2 个图片，发送给指定收件人
同时发送 2 种可选正文，发送内嵌图片，发送附件

Author: 仗剑天涯
Date:2026/4/19

注意：API 密钥和邮箱配置从 .env 文件读取
"""

import os
import sys
import requests
from pathlib import Path
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from urllib.parse import quote

from utils.config_helper import get_pexels_api_key, get_email_config

# ==================== 配置区域 ====================
PEXELS_API_KEY = get_pexels_api_key()
EMAIL_CONFIG = get_email_config()
QUERY = "woman"          # 搜索关键词
COUNT = 2                # 需要下载的图片数量
# =================================================

def creat_attachment(path, filename):
    _filename = filename
    _char = '/'
    if path == '':
        _char = ''
    with open(f'{path}{_char}{_filename}', 'rb') as foo:
        att2 = MIMEText(foo.read(), 'base64', 'utf-8')
        # 指定内容类型 - 附件
        att2["Content-Type"] = 'application/octet-stream'
        # 如果函数有中文，需要处理成百分号编码 (
        # 收到邮件中显示百分号编码，但是下载到本地时，文件名会正确显示)
        _filename = quote(_filename)
        # 指定处理方式 - 下载
        att2["Content-Disposition"] = f'attachment; filename="{_filename}"'
        return att2


def search_pexels_images(query: str, per_page: int = 10) -> list:
    """
    使用 Pexels API 搜索图片。

    Args:
        query: 搜索关键词
        per_page: 每页返回的图片数量（默认 10，最大 80）

    Returns:
        包含图片信息的列表，每个元素为 dict
    """
    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": query,
        "per_page": per_page
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data.get("photos", [])
    except requests.exceptions.RequestException as e:
        print(f"❌ API 请求失败：{e}")
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
        img_response = requests.get(image_url, timeout=20)
        img_response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(img_response.content)

        print(f"✅ 已保存：{save_path.name}")
        return True

    except Exception as e:
        print(f"❌ 下载失败 {image_url}: {e}")
        return False


def main():
    """主函数：搜索图片并下载到桌面"""
    # 检查 API 密钥是否已配置
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY_HERE":
        print("⚠️ 请先复制 .env.example 为 .env 并填写你的 Pexels API 密钥")
        return
    
    # 检查邮箱配置
    if EMAIL_CONFIG['sender'] == "your_email@163.com":
        print("⚠️ 请先在 .env 文件中配置你的邮箱信息")
        return

    # 1. 确定桌面路径（兼容 Windows / macOS / Linux）
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        desktop = Path.home() / "桌面"
    if not desktop.exists():
        print("❌ 无法定位桌面路径，请手动指定保存目录。")
        return

    print(f"🔍 正在 Pexels 搜索关键词 '{QUERY}' ...")
    photos = search_pexels_images(QUERY, per_page=COUNT * 2)

    if not photos:
        print("❌ 未搜索到任何图片，请检查网络或 API 密钥是否有效。")
        return

    # 2. 下载前 COUNT 张有效图片
    downloaded = 0
    name_list = []
    path_list = []
    for i, photo in enumerate(photos):
        if downloaded >= COUNT:
            break

        src_info = photo.get("src", {})
        img_url = src_info.get("original") or src_info.get("large2x") or src_info.get("large")

        if not img_url:
            print(f"⚠️ 第 {i+1} 张图片缺少有效 URL，跳过。")
            continue

        ext = ".jpg"
        if ".png" in img_url.lower():
            ext = ".png"

        filename = f"pexels_{QUERY}_{downloaded+1:02d}{ext}"
        save_path = desktop / filename
        path_list.append(desktop)
        name_list.append(filename)

        if download_image(img_url, save_path):
            downloaded += 1

    print(f"\n🎉 完成！共成功下载 {downloaded} 张图片到桌面：{desktop}")

    sender = EMAIL_CONFIG['sender']
    receivers = [EMAIL_CONFIG['default_receiver']]

    # 创建邮件对象
    email = MIMEMultipart('related')
    email['From'] = formataddr((str(Header('西门吹雪', 'utf-8')), sender))
    email['To'] = formataddr((str(Header('叶孤城', 'utf-8')), receivers[0]))
    email['Subject'] = Header('月圆之夜，紫禁之巅，来战！')

    msgAlternative = MIMEMultipart('alternative')
    email.attach(msgAlternative)
    mail_msg = """
    <p>Python 邮件发送测试...</p>
    <p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
    <p>图片演示：</p>
    <p><img src="cid:image1"></p>
    """
    msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
    
    fp = open('resources/888.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    email.attach(msgImage)
    
    email.attach(creat_attachment('', '一年级二班考试成绩表 2.xlsx'))
    email.attach(creat_attachment('', '离职证明 3.docx'))
    email.attach(creat_attachment('resources', '演示 PPT.pptx'))
    email.attach(creat_attachment('resources', '888.png'))
    email.attach(creat_attachment(path_list[0], name_list[0]))
    email.attach(creat_attachment(path_list[1], name_list[1]))
    email.attach(creat_attachment('resources', 'pexels_video_1409899_Michal Marek.mp4'))

    smtp_obj = smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
    smtp_obj.login(sender, EMAIL_CONFIG['password'])
    smtp_obj.sendmail(sender, receivers, email.as_string())


if __name__ == "__main__":
    main()
