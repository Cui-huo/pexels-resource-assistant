"""
小脚本 -
从图片网站pexels的api上下载图片并保存
Author:仗剑天涯
Date:2026/4/15
"""
import os.path

import requests

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
        print(f"✅ 已下载: {filename}")
    except Exception as e:
        print(f"❌ 下载失败: {filename}，错误信息: {e}")

def main():
    # 1. 检查并创建存放图片的文件夹
    save_dir = 'my_pictures/example_images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"📁 文件夹已创建: {save_dir}")

    # 2. 你的 Pexels API 密钥（请确保密钥有效）
    API_KEY = "gH0PMN2NOO6vJuLGK6x3WhKa5H2As3ww9wr5ovGhxLrS0efspR6NmuHv"

    # 3. 定义官方 API 端点 (Endpoint)
    #    这里是「精选热门图片」接口，per_page=2 表示每次获取 2 张图片
    #    如果想搜索特定内容，可以将 url 换成:
    #    url = "https://api.pexels.com/v1/search?query=猫&per_page=2"
    url = "https://api.pexels.com/v1/curated?per_page=10"

    # 4. 关键步骤：将 API 密钥添加到请求头 (Request Headers) 中
    #    Pexels 的认证方式就是在 Headers 里加上 "Authorization": "你的密钥"
    headers = {
        "Authorization": API_KEY
    }

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
            # 可选尺寸有: 'original', 'large', 'medium', 'small' 等
            # 这里选择 'large' 尺寸，清晰度够用且下载速度快
            image_url = photo['src']['large']
            print(f"🔗 图片链接: {image_url}")
            # 调用之前写好的下载函数，将图片保存到本地
            download_picture(save_dir, image_url)

    except requests.exceptions.RequestException as e:
        # 捕获所有网络请求相关的异常
        print(f"❌ API 请求出错: {e}")
    except KeyError as e:
        # 如果返回的 JSON 结构不符合预期，可能缺少某些字段
        print(f"❌ 解析返回数据时出错，缺少字段: {e}")

"""def download_picture(path, url):
    filename = url[url.rfind('/') + 1:].split('?')[0]
    print(filename,path)
    resp = requests.get(url)
    with open(f'{path}/{filename}', 'wb') as file:
        file.write(resp.content)

def main():
    if not os.path.exists('my_pictures/example_images'):
        os.makedirs('my_pictures/example_images')

    # 1. 你的 API 密钥
    API_KEY = "gH0PMN2NOO6vJuLGK6x3WhKa5H2As3ww9wr5ovGhxLrS0efspR6NmuHv"  # 请把 'YOUR_PEXELS_API_KEY' 替换成你的真实密钥

    # 2. 定义正确的 API 端点 (API Endpoint)
    # 这是 '获取热门图片' 的接口，per_page=2 表示获取 2 张图片
    url = "https://api.pexels.com/v1/curated?per_page=10"

    # 3. 关键步骤：将 API 密钥添加到请求头 (Request Headers) 中
    headers = {
        "Authorization": "gH0PMN2NOO6vJuLGK6x3WhKa5H2As3ww9wr5ovGhxLrS0efspR6NmuHv"  # 格式就是 Authorization: YOUR_API_KEY
    }

    # 4. 发起请求
    response = requests.get(url, headers=headers)
    print(response)
    response.raise_for_status()
    data = response.json()
    print(data)
    photos_list = data['photos']
    for photo_dict in photos_list:
        # 官方返回结构中，图片链接在 photo['src'] 里，有多种尺寸可选
        # 这里选择 'large' 尺寸（较大但比 original 小，下载更快）
        image_url = photo_dict['src']['large']
        print(f"图片链接: {image_url}")
        download_picture('resources', image_url)"""


if __name__ == '__main__':
    main()




"""
{'page': 1, 'per_page': 10, 'photos': [
{'id': 36597363, 'width': 3840, 'height': 5760, 
'url': 'https://www.pexels.com/photo/charming-alleyway-view-of-bari-harbor-at-twilight-36597363/', 'photographer': 'Leonardo Delsabio', 'photographer_url': 'https://www.pexels.com/@leonardo-delsabio-2150529415', 'photographer_id': 2150529415, 'avg_color': '#5D4A43', 'src': {'original': 'https://images.pexels.com/photos/36597363/pexels-photo-36597363.jpeg', 'large2x': 'https://images.pexels.com/photos/36597363/pexels-photo-36597363.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', 'large': 'https://images.pexels.com/photos/36597363/pexels-photo-36597363.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', 'medium': 'https://images.pexels.com/photos/36597363/pexels-photo-36597363.jpeg?auto=compress&cs=tinysrgb&h=350', 'small': 'https://images.pexels.com/photos/36597363/pexels-photo-36597363.jpeg?auto=compress&cs=tinysrgb&h=130', 'portrait': 'https://images.pexels.com/photos/36597363/pexels-photo-36597363.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800', 'landscape': 'https://images.pexels.com/photos/36597363/pexels-photo-36597363.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200',
 'tiny': 'https://images.pexels.com/photos/36597363/pexels-photo-36597363.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280'}, 
 'liked': False, 'alt': 'Unique view of Bari Harbor through a charming alleyway, illuminated at twilight.'}, 
 {'id': 29590677, 'width': 3971, 'height': 5956, 'url': 'https://www.pexels.com/photo/charming-dog-walking-on-a-forest-path-29590677/', 'photographer': 'Michał Robak', 'photographer_url': 'https://www.pexels.com/@michalrobak', 'photographer_id': 537686181, 'avg_color': '#736D61', 
 'src': {'original': 'https://images.pexels.com/photos/29590677/pexels-photo-29590677.jpeg', 'large2x': 'https://images.pexels.com/photos/29590677/pexels-photo-29590677.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', 'large': 'https://images.pexels.com/photos/29590677/pexels-photo-29590677.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', 'medium': 'https://images.pexels.com/photos/29590677/pexels-photo-29590677.jpeg?auto=compress&cs=tinysrgb&h=350', 'small': 'https://images.pexels.com/photos/29590677/pexels-photo-29590677.jpeg?auto=compress&cs=tinysrgb&h=130', 'portrait': 'https://images.pexels.com/photos/29590677/pexels-photo-29590677.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800', 'landscape': 'https://images.pexels.com/photos/29590677/pexels-photo-29590677.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200', 'tiny': 'https://images.pexels.com/photos/29590677/pexels-photo-29590677.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280'}, 'liked': False, 'alt': 'A fluffy dog joyfully walks down a serene forest path, embodying freedom and adventure.'},
  {'id': 36672413, 'width': 3707, 'height': 4943, 'url': 'https://www.pexels.com/photo/authentic-italian-cuisine-at-la-gavitella-36672413/', 'photographer': 'ludo s', 'photographer_url': 'https://www.pexels.com/@ludo-s-2160368771', 'photographer_id': 2160368771, 'avg_color': '#8A6C50', 'src': {'original': 'https://images.pexels.com/photos/36672413/pexels-photo-36672413.jpeg', 'large2x': 'https://images.pexels.com/photos/36672413/pexels-photo-36672413.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', 'large': 'https://images.pexels.com/photos/36672413/pexels-photo-36672413.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', 'medium': 'https://images.pexels.com/photos/36672413/pexels-photo-36672413.jpeg?auto=compress&cs=tinysrgb&h=350', 'small': 'https://images.pexels.com/photos/36672413/pexels-photo-36672413.jpeg?auto=compress&cs=tinysrgb&h=130', 'portrait': 'https://images.pexels.com/photos/36672413/pexels-photo-36672413.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800', 'landscape': 'https://images.pexels.com/photos/36672413/pexels-photo-36672413.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200', 'tiny': 'https://images.pexels.com/photos/36672413/pexels-photo-36672413.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280'}, 'liked': False, 'alt': 'Discover delicious Italian dishes at La Gavitella in Praiano, Italy, featuring vibrant pasta and refreshing drinks.'}, {'id': 36421419, 'width': 2048, 'height': 2995, 'url': 'https://www.pexels.com/photo/autumn-colors-in-scenic-tea-plantation-36421419/', 'photographer': 'Linh Tran', 'photographer_url': 'https://www.pexels.com/@linh-tran-553086511', 'photographer_id': 553086511, 'avg_color': '#483329', 'src': {'original': 'https://images.pexels.com/photos/36421419/pexels-photo-36421419.png', 'large2x': 'https://images.pexels.com/photos/36421419/pexels-photo-36421419.png?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', 'large': 'https://images.pexels.com/photos/36421419/pexels-photo-36421419.png?auto=compress&cs=tinysrgb&h=650&w=940', 'medium': 'https://images.pexels.com/photos/36421419/pexels-photo-36421419.png?auto=compress&cs=tinysrgb&h=350', 'small': 'https://images.pexels.com/photos/36421419/pexels-photo-36421419.png?auto=compress&cs=tinysrgb&h=130', 'portrait': 'https://images.pexels.com/photos/36421419/pexels-photo-36421419.png?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800', 'landscape': 'https://images.pexels.com/photos/36421419/pexels-photo-36421419.png?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200', 'tiny': 'https://images.pexels.com/photos/36421419/pexels-photo-36421419.png?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280'}, 'liked': False, 'alt': 'Vibrant autumn trees in a terraced tea plantation create a stunning landscape.'}, {'id': 20269668, 'width': 3024, 'height': 4032, 'url': 'https://www.pexels.com/photo/cute-dog-and-a-bouquet-of-roses-on-a-bed-20269668/', 'photographer': 'anna.sorohan_ph', 'photographer_url': 'https://www.pexels.com/@anna-sorohan_ph-950571252', 'photographer_id': 950571252, 'avg_color': '#A2948B', 'src': {'original': 'https://images.pexels.com/photos/20269668/pexels-photo-20269668.jpeg', 'large2x': 'https://images.pexels.com/photos/20269668/pexels-photo-20269668.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', 'large': 'https://images.pexels.com/photos/20269668/pexels-photo-20269668.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', 'medium': 'https://images.pexels.com/photos/20269668/pexels-photo-20269668.jpeg?auto=compress&cs=tinysrgb&h=350', 'small': 'https://images.pexels.com/photos/20269668/pexels-photo-20269668.jpeg?auto=compress&cs=tinysrgb&h=130', 'portrait': 'https://images.pexels.com/photos/20269668/pexels-photo-20269668.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800', 'landscape': 'https://images.pexels.com/photos/20269668/pexels-photo-20269668.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200', 'tiny': 'https://images.pexels.com/photos/20269668/pexels-photo-20269668.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280'}, 'liked': False, 'alt': 'A cute small dog sits beside a vibrant bouquet of roses on a white bedspread indoors.'}, {'id': 20518745, 'width': 3276, 'height': 4096, 'url': 'https://www.pexels.com/photo/street-and-buildings-in-berlin-in-germany-20518745/', 'photographer': 'Meike', 'photographer_url': 'https://www.pexels.com/@meike-664865296', 'photographer_id': 664865296, 'avg_color': '#655B59', 
  'src': {'original': 'https://images.pexels.com/photos/20518745/pexels-photo-20518745.jpeg', 'large2x': 'https://images.pexels.com/photos/20518745/pexels-photo-20518745.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', 'large': 'https://images.pexels.com/photos/20518745/pexels-photo-20518745.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', 'medium': 'https://images.pexels.com/photos/20518745/pexels-photo-20518745.jpeg?auto=compress&cs=tinysrgb&h=350', 'small': 'https://images.pexels.com/photos/20518745/pexels-photo-20518745.jpeg?auto=compress&cs=tinysrgb&h=130', 'portrait': 'https://images.pexels.com/photos/20518745/pexels-photo-20518745.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800', 'landscape': 'https://images.pexels.com/photos/20518745/pexels-photo-20518745.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200', 'tiny': 'https://images.pexels.com/photos/20518745/pexels-photo-20518745.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280'}, 'liked': False, 'alt': 'Charming Berlin city street with parked cars and classic architecture at sunset.'}, {'id': 36739215, 'width': 3598, 'height': 4498, 'url': 'https://www.pexels.com/photo/charming-sunlit-arcades-of-modena-italy-36739215/', 'photographer': 'Grigorii Shcheglov', 'photographer_url': 'https://www.pexels.com/@grigorii-shcheglov-2160104994', 'photographer_id': 2160104994, 'avg_color': '#BE864D', 'src': {'original': 'https://images.pexels.com/photos/36739215/pexels-photo-36739215.jpeg', 'large2x': 'https://images.pexels.com/photos/36739215/pexels-photo-36739215.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', 'large': 'https://images.pexels.com/photos/36739215/pexels-photo-36739215.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', 'medium': 'https://images.pexels.com/photos/36739215/pexels-photo-36739215.jpeg?auto=compress&cs=tinysrgb&h=350', 'small': 'https://images.pexels.com/photos/36739215/pexels-photo-36739215.jpeg?auto=compress&cs=tinysrgb&h=130', 'portrait': 'https://images.pexels.com/photos/36739215/pexels-photo-36739215.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800', 'landscape': 'https://images.pexels.com/photos/36739215/pexels-photo-36739215.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200', 'tiny': 'https://images.pexels.com/photos/36739215/pexels-photo-36739215.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280'}, 'liked': False, 'alt': 'Sunlit arcades with arches in Modena, Italy, showcasing classic Italian architecture.'}, {'id': 36464894, 'width': 6499, 'height': 4333, 'url': 'https://www.pexels.com/photo/vibrant-flower-stall-display-on-hanoi-street-36464894/', 'photographer': 'Hung Pham', 'photographer_url': 'https://www.pexels.com/@hung-pham-1332058235', 'photographer_id': 1332058235, 'avg_color': '#7C6E65', 'src': {'original': 'https://images.pexels.com/photos/36464894/pexels-photo-36464894.jpeg', 'large2x': 'https://images.pexels.com/photos/36464894/pexels-photo-36464894.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', 'large': 'https://images.pexels.com/photos/36464894/pexels-photo-36464894.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', 'medium': 'https://images.pexels.com/photos/36464894/pexels-photo-36464894.jpeg?auto=compress&cs=tinysrgb&h=350', 'small': 'https://images.pexels.com/photos/36464894/pexels-photo-36464894.jpeg?auto=compress&cs=tinysrgb&h=130', 'portrait': 'https://images.pexels.com/photos/36464894/pexels-photo-36464894.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800', 'landscape': 'https://images.pexels.com/photos/36464894/pexels-photo-36464894.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200', 'tiny': 'https://images.pexels.com/photos/36464894/pexels-photo-36464894.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280'}, 'liked': False, 'alt': 'Colorful flower stall with diverse floral bouquets on a street in Hanoi, Vietnam.'}, {'id': 35927296, 'width': 6000, 'height': 4000, 'url': 'https://www.pexels.com/photo/golden-sunset-over-hamilton-s-silhouetted-trees-35927296/', 'photographer': 'Chiara Holzhaeuser', 'photographer_url': 'https://www.pexels.com/@chiara-holzhaeuser-2157516733', 'photographer_id': 2157516733, 'avg_color': '#824912', 'src': {'original': 'https://images.pexels.com/photos/35927296/pexels-photo-35927296.jpeg', 'large2x': 'https://images.pexels.com/photos/35927296/pexels-photo-35927296.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', 'large': 'https://images.pexels.com/photos/35927296/pexels-photo-35927296.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', 'medium': 'https://images.pexels.com/photos/35927296/pexels-photo-35927296.jpeg?auto=compress&cs=tinysrgb&h=350', 'small': 'https://images.pexels.com/photos/35927296/pexels-photo-35927296.jpeg?auto=compress&cs=tinysrgb&h=130', 'portrait': 'https://images.pexels.com/photos/35927296/pexels-photo-35927296.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800', 'landscape': 'https://images.pexels.com/photos/35927296/pexels-photo-35927296.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200', 'tiny': 'https://images.pexels.com/photos/35927296/pexels-photo-35927296.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280'}, 'liked': False, 'alt': 'Vibrant sunset with golden clouds and silhouetted trees in Hamilton, VIC.'}, {'id': 29885765, 'width': 4000, 'height': 6000, 'url': 'https://www.pexels.com/photo/man-standing-in-a-vintage-alleyway-in-ho-chi-minh-city-29885765/', 'photographer': 'Theodore Nguyen', 'photographer_url': 'https://www.pexels.com/@thejourneyofframes', 'photographer_id': 898884684, 'avg_color': '#5E563F', 'src': {'original': 'https://images.pexels.com/photos/29885765/pexels-photo-29885765.jpeg', 'large2x': 'https://images.pexels.com/photos/29885765/pexels-photo-29885765.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', 'large': 'https://images.pexels.com/photos/29885765/pexels-photo-29885765.jpeg?auto=compress&cs=tinysrgb&h=650&w=940', 'medium': 'https://images.pexels.com/photos/29885765/pexels-photo-29885765.jpeg?auto=compress&cs=tinysrgb&h=350', 'small': 'https://images.pexels.com/photos/29885765/pexels-photo-29885765.jpeg?auto=compress&cs=tinysrgb&h=130', 'portrait': 'https://images.pexels.com/photos/29885765/pexels-photo-29885765.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800', 'landscape': 'https://images.pexels.com/photos/29885765/pexels-photo-29885765.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200', 'tiny': 'https://images.pexels.com/photos/29885765/pexels-photo-29885765.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280'}, 'liked': False, 'alt': 'Portrait of a young man in a vintage alleyway with vibrant lighting in Ho Chi Minh City, Vietnam.'}], 'total_results': 62698, 'next_page': 'https://api.pexels.com/v1/v1/curated?page=2&per_page=10'}
"""