"""
小脚本 -
从图片网站 pexels 的 api 上下载图片并保存
Author: 仗剑天涯
Date:2026/4/15

注意：API 密钥从 download_and_send/config.py 导入，请勿硬编码
"""
import os
import sys
import requests
from pathlib import Path

# 添加项目根目录到路径，以便导入 config
sys.path.insert(0, str(Path(__file__).parent / 'download_and_send'))
from config import PEXELS_API_KEY

def download_picture(path, url):
    """
    下载图片并保存到指定文件夹
    :param path: 保存路径 (如 'my_pictures/example_images/')
    :param url: 图片的直链地址
    """
    # 从 URL 中提取文件名 (例如 'pexels-photo-xxxxx.jpeg')
    # split('/')[-1] 取最后一个 '/' 后面的部分，再用 split('?')[0] 去掉可能的 URL 参数
    filename = url.split('/')[-1].split('?')[0]
    # 用 os.path.join 拼接完整路径，避免手动处理斜杠问题
    filepath = os.path.join(path, filename)

    try:
        # 发送 GET 请求下载图片内容，timeout=30 防止长时间卡住
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()  # 如果状态码不是 200，直接抛出异常

        # 以二进制写入模式保存文件
        with open(filepath, 'wb') as file:
            file.write(resp.content)
        print(f"✅ 已下载：{filename}")
    except Exception as e:
        print(f"❌ 下载失败：{filename}，错误信息：{e}")

def main():
    # 1. 检查并创建存放图片的文件夹
    save_dir = 'my_pictures/example_images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"📁 文件夹已创建：{save_dir}")

    # 2. 定义官方 API 端点 (Endpoint)
    #    这里是「精选热门图片」接口，per_page=2 表示每次获取 2 张图片
    #    如果想搜索特定内容，可以将 url 换成:
    #    url = "https://api.pexels.com/v1/search?query=猫&per_page=2"
    url = "https://api.pexels.com/v1/curated?per_page=10"

    # 3. 关键步骤：将 API 密钥添加到请求头 (Request Headers) 中
    #    Pexels 的认证方式就是在 Headers 里加上 "Authorization": "你的密钥"
    headers = {
        "Authorization": PEXELS_API_KEY  # 从 config.py 导入
    }

    # 4. 关键步骤：检查 API 密钥是否已配置
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY_HERE":
        print("⚠️ 请先在 download_and_send/config.py 或 .env 文件中配置你的 Pexels API 密钥")
        print("获取方式：登录 https://www.pexels.com/api/ 申请")
        return

    # 5. 发起 GET 请求调用 API
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # 检查 HTTP 状态，200 才继续
        data = response.json()       # 将返回的 JSON 字符串解析成 Python 字典

        # 6. 提取图片信息
        #    官方返回的数据结构里，图片列表在 'photos' 这个 key 下面
        photos = data.get('photos', [])
        if not photos:
            print("⚠️ 没有获取到任何图片，可能是 API 配额用完了或者网络问题。")
            return

        # 7. 遍历图片列表，取出下载链接并调用下载函数
        for photo in photos:
            # 每张图片的详细链接都放在 photo['src'] 里面
            # 可选尺寸有：'original', 'large', 'medium', 'small' 等
            # 这里选择 'large' 尺寸，清晰度够用且下载速度快
            image_url = photo['src']['large']
            print(f"🔗 图片链接：{image_url}")
            # 调用之前写好的下载函数，将图片保存到本地
            download_picture(save_dir, image_url)

    except requests.exceptions.RequestException as e:
        # 捕获所有网络请求相关的异常
        print(f"❌ API 请求出错：{e}")
    except KeyError as e:
        # 如果返回的 JSON 结构不符合预期，可能缺少某些字段
        print(f"❌ 解析返回数据时出错，缺少字段：{e}")


if __name__ == '__main__':
    main()
