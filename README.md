# 🚀 Pexels 资源助手

一个基于 Python 的 Pexels 资源下载和邮件发送工具，支持从 Pexels 平台搜索和下载高清图片、视频资源，并可通过 SMTP 协议发送邮件（支持附件拖拽）。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Pexels API](https://img.shields.io/badge/Pexels-API-orange.svg)

## ✨ 功能特性

### 📸 图片下载
- 支持关键词搜索图片
- 支持下载热门精选图片
- 自动保存至本地 `downloads` 目录
- 可自定义下载数量

### 🎬 视频下载
- 支持关键词搜索视频
- 支持下载热门视频
- 智能选择视频分辨率（优先下载较小文件，节省时间）
- 自动保存至本地 `downloads` 目录

### 📧 邮件发送
- **发送已下载的 Pexels 资源**：从下载目录中选择文件或全部发送
- **发送本地任意文件**：支持拖拽文件到窗口自动识别路径
- 支持多附件发送（用逗号分隔多个文件路径）
- 支持 HTML 正文和内嵌图片
- 中文文件名自动编码处理

## 📦 安装

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/pexels-helper.git
cd pexels-helper
```

### 2. 创建虚拟环境（可选但推荐）

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 🔧 验证安装

在开始使用前，运行测试脚本确认环境配置正确：

```bash
python test_setup.py
```

✅ 所有测试通过后，即可正常使用主程序。

---

## ⚙️ 配置

### 1. 复制环境变量模板

```bash
# Windows (PowerShell)
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

### 2. 编辑 .env 文件

在 `.env` 文件中填入你的真实配置：

```bash
# Pexels API Key（登录 https://www.pexels.com/api/ 申请）
PEXELS_API_KEY=your_pexels_api_key_here

# 邮箱配置（以 163 邮箱为例）
EMAIL_SENDER=your_email@163.com
EMAIL_PASSWORD=your_smtp_auth_code    # 注意：是授权码，不是登录密码！
SMTP_SERVER=smtp.163.com
SMTP_PORT=465
DEFAULT_RECEIVER=receiver@example.com
```

> **如何获取邮箱授权码**：  
> 登录网易邮箱 → 设置 → POP3/SMTP/IMAP → 开启 SMTP 服务并获取授权码。

## 🚀 使用方法

### 方式一：命令行运行

```bash
cd download_and_send
python main.py
```

### 方式二：打包为 EXE（Windows）

项目已包含打包配置文件 `main.spec`，使用 PyInstaller 打包：

```bash
pip install pyinstaller
pyinstaller main.spec
```

生成的可执行文件位于 `dist/main.exe`。

### 主菜单功能

运行程序后将显示以下菜单：

```
==================================================
   🚀 Pexels 资源助手 - 主菜单
==================================================
1. 下载和搜索图片
2. 下载和搜索视频
3. 发送已下载的 Pexels 文件到邮箱
4. 发送本地任意文件到邮箱
5. 退出程序
```

#### 功能说明

1. **下载和搜索图片**
   - 输入关键词搜索或直接下载热门图片
   - 指定下载数量
   - 自动保存到 `downloads` 目录

2. **下载和搜索视频**
   - 输入关键词搜索或直接下载热门视频
   - 指定下载数量
   - 自动保存到 `downloads` 目录

3. **发送已下载的 Pexels 文件到邮箱**
   - 列出 `downloads` 目录中所有文件和大小
   - 支持选择单个或多个文件（编号用逗号分隔）
   - 直接回车发送全部文件

4. **发送本地任意文件到邮箱**
   - 支持拖拽文件到窗口自动填入路径
   - 支持多个文件路径（用英文逗号分隔）
   - 自动验证文件是否存在

## 📁 项目结构

```
Day14/
├── download_and_send/           # 主要功能模块（核心）
│   ├── main.py                  # 主程序入口
│   ├── config.py                # 配置文件（从 .env 读取敏感信息）
│   ├── download_pictures_and_videos.py  # 图片视频下载功能
│   ├── send_email.py            # 邮件发送功能
│   └── downloads/               # 下载文件存储目录（已忽略）
├── download_from_pexels.py      # 独立图片下载脚本（早期版本）
├── download_pictures.py         # 独立图片下载脚本
├── download_video_from_pexels.py # 独立视频下载脚本
├── email_extend.py              # 图片 API 下载示例
├── send_email_.py               # 基础邮件发送示例
├── send_email_pictures_from_pexels.py  # 综合示例脚本
├── send_my_email.py             # 邮件发送学习脚本
├── .env.example                 # 环境变量模板（复制为 .env 使用）
├── .gitignore                   # Git 忽略规则
├── requirements.txt             # Python 依赖列表
├── README.md                    # 项目文档
└── LICENSE                      # MIT 许可证
```

> **说明**：`resources/`、`videos/`、`my_pictures/` 等文件夹包含示例资源文件，体积较大，已在 `.gitignore` 中排除。

## 🔧 依赖

- `requests` - HTTP 请求库，用于调用 Pexels API
- `python-dotenv` - 环境变量管理，从 .env 文件读取配置
- `openpyxl` - Excel 文件处理（可选）
- `pillow` - 图像处理（可选）

完整依赖请见 `requirements.txt`。

## 📝 示例

### 下载 5 张"cat"主题图片

```
请输入选项 (1/2/3/4/5): 1
📸 图片下载子菜单
1. 关键词搜索图片
2. 直接下载热门图片
请选择 (1/2/3): 1
请输入搜索关键词：cat
请输入要下载的图片数量：5
```

### 发送本地文件（支持拖拽）

```
请输入选项 (1/2/3/4/5): 4
📎 发送本地文件
💡 提示：可以直接将文件拖拽到本窗口，自动填入路径
请输入文件路径（多个用逗号分隔）: C:\Users\test\Desktop\photo.jpg, C:\Users\test\Desktop\video.mp4
```

## ⚠️ 注意事项

1. **API 限制**：Pexels 免费 API 有速率限制，请勿短时间内大量请求
2. **邮箱安全**：`.env` 文件包含敏感信息，切勿上传至公开仓库
3. **文件清理**：下载的临时文件请及时清理，避免占用过多磁盘空间
4. **兼容性**：已在 Windows 上测试通过，macOS/Linux 需调整部分路径处理
5. **隐私保护**：项目已配置 `.gitignore`，自动排除敏感文件和大体积资源文件夹

## 📄 License

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

- Author: Cui-huo
- Email: heiye0.0duxing@gmail.com
- GitHub: https://github.com/Cui-huo

---

Made with ❤️ by Cui-huo
