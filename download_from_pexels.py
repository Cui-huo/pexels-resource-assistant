"""
download_from_pexels -
用我自己的账号密钥，获取图片或者视频数据
（我人生的第一个正式 API 调用脚本）

Author: 仗剑天涯
Date:2026/4/16

注意：API 密钥从 .env 文件读取，请先复制 .env.example 为 .env 并配置
"""
import os
from pathlib import Path
from pprint import pprint
import requests
from utils.config_helper import get_pexels_api_key, get_output_dir


def download_one_picture(url, path, index):
    try:
        # 根据 url 获取对象，写入文件
        response = requests.get(url, timeout=30)
        # 检查状态码是否异常
        response.raise_for_status()
        try:
            # 用 split 函数把字符串分割成列表，取第一个元素为文件名
            filename = url[url.rfind('/') + 1:].split('?')[0]
            if not filename:
                raise ValueError
        except:
            filename = f"image_{index}.jpg"
            print(f'从 url 获取文件名{filename}异常')
        # 检查存储路径，如果没有则创建
        if not os.path.exists(path):
            os.makedirs(path)
        # 拼接文件路径
        filepath = os.path.join(path, filename)
        with open(filepath, 'wb') as file:
            print(f'第{index+1}张图片下载成功{filename}')
            file.write(response.content)
        return True
    except Exception as e:
        print(f'图片下载失败，错误信息：{url}->{e}')
        return False


def main():
    # 从 .env 文件获取 API Key
    PEXELS_API_KEY = get_pexels_api_key()
    
    # 检查 API 密钥是否已配置
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY_HERE":
        print("⚠️ 请先复制 .env.example 为 .env 并填写你的 Pexels API 密钥")
        print("获取方式：登录 https://www.pexels.com/api/ 申请")
        return
    
    headers = {'Authorization': PEXELS_API_KEY}
    url = "https://api.pexels.com/v1/search"
    
    # 3. 设置搜索参数
    params = {
        "query": "beautiful girls",  # 搜索关键词（必填）
        "per_page": 30,  # 每页数量，默认 15，最大 80
        "page": 2  # 页码，默认 1
    }
    # 从官方接口调用数据
    responses = requests.get(url, headers=headers, params=params, timeout=300)
    # 检查状态码
    responses.raise_for_status()
    # 把 json 数据转化为字典 data
    data = responses.json()
    # Python 内置模块，专门用于美化打印 Python 对象。
    # indent=2：缩进空格数。width=80：每行最大宽度，超过会自动换行。
    pprint(data, indent=2, width=80)

    # 从 data 字典中解析数据
    photos_list = data['photos']
    counter = 0
    counter2 = 0
    # 遍历取 photo_dict 对象
    for index, photo_dict in enumerate(photos_list):
        # 安全获取中等尺寸图片 URL
        url = photo_dict.get('src', {}).get('medium')
        if not url:
            print(f"第 {index + 1} 张图片缺少 medium URL，跳过")
            continue

        path = get_output_dir('download_pictures/pexel')
        flag = download_one_picture(url, str(path), index)
        if flag:
            counter += 1
        counter2 = index if counter2 < index else counter2
    print(f'下载成功{counter}张，失败{counter2+1-counter}张')


if __name__ == '__main__':
    main()
