"""
小脚本 -
从图片网站 pexels 的 api 上下载图片并保存

Author: 仗剑天涯
Date:2026/4/15

注意：API 密钥从 .env 文件读取，请先复制 .env.example 为 .env 并配置
"""
import os
import requests
from utils.config_helper import get_pexels_api_key, get_output_dir

def download_picture(path, url):
    """
    下载图片并保存到指定文件夹
    :param path: 保存路径 (如 'my_pictures/example_images/')
    :param url: 图片的直链地址
    """
    # 从 URL 中提取文件名 (例如 'pexels-photo-xxxxx.jpeg')
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
    save_dir = get_output_dir('my_pictures/example_images')
    print(f"📁 文件夹已创建：{save_dir}")

    # 2. 获取 API Key
    PEXELS_API_KEY = get_pexels_api_key()
    
    # 3. 检查 API 密钥是否已配置
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY_HERE":
        print("⚠️ 请先复制 .env.example 为 .env 并填写你的 Pexels API 密钥")
        print("获取方式：登录 https://www.pexels.com/api/ 申请")
        return

    # 4. 定义官方 API 端点 (Endpoint)
    url = "https://api.pexels.com/v1/curated?per_page=10"

    # 5. 关键步骤：将 API 密钥添加到请求头 (Request Headers) 中
    headers = {
        "Authorization": PEXELS_API_KEY
    }

    # 6. 发起 GET 请求调用 API
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # 检查 HTTP 状态，200 才继续
        data = response.json()       # 将返回的 JSON 字符串解析成 Python 字典

        # 7. 提取图片信息
        photos = data.get('photos', [])
        if not photos:
            print("⚠️ 没有获取到任何图片，可能是 API 配额用完了或者网络问题。")
            return

        # 8. 遍历图片列表，取出下载链接并调用下载函数
        for photo in photos:
            image_url = photo['src']['large']
            print(f"🔗 图片链接：{image_url}")
            download_picture(str(save_dir), image_url)

    except requests.exceptions.RequestException as e:
        print(f"❌ API 请求出错：{e}")
    except KeyError as e:
        print(f"❌ 解析返回数据时出错，缺少字段：{e}")


if __name__ == '__main__':
    main()
