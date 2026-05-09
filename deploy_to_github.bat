@echo off
chcp 65001 >nul
echo ========================================
echo   🚀 Pexels 资源助手 - GitHub 发布脚本
echo ========================================
echo.

:: 检查 git 是否已安装
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未检测到 Git，请先安装 Git
    echo 下载地址：https://git-scm.com/
    pause
    exit /b 1
)

:: 配置 Git 用户信息
echo ⚙️  正在配置 Git 用户信息...
git config user.name "Cui-huo"
git config user.email "heiye0.0duxing@gmail.com"
echo ✅ Git 用户信息已设置

:: 初始化仓库（如果尚未初始化）
if not exist .git (
    echo 📦 正在初始化 Git 仓库...
    git init
)

:: 添加所有文件
echo 📂 正在添加文件到暂存区...
git add .

:: 显示将要提交的文件
echo.
echo 📋 以下文件将被提交：
git status --short

:: 确认提交
echo.
set /p confirm="确认提交到本地仓库？(Y/N): "
if /i not "%confirm%"=="Y" (
    echo ❌ 操作已取消
    pause
    exit /b 1
)

:: 提交更改
echo 💾 正在提交到本地仓库...
git commit -m "Initial commit: Pexels 资源助手 v1.0

功能特性:
- 从 Pexels 下载图片和视频
- 支持关键词搜索和热门资源
- SMTP 邮件发送（支持附件拖拽）
- 多文件批量发送

作者：Cui-huo
邮箱：heiye0.0duxing@gmail.com"

:: 添加远程仓库（需要用户手动替换 URL）
echo.
echo 🔗 请设置你的 GitHub 仓库地址
echo 示例：https://github.com/Cui-huo/pexels-helper.git
set /p repo_url="输入 GitHub 仓库 URL (直接回车跳过): "
if not "%repo_url%"=="" (
    git remote remove origin 2>nul
    git remote add origin %repo_url%
    echo ✅ 远程仓库已设置：%repo_url%
    
    :: 推送到 GitHub
    echo.
    echo 🚀 正在推送到 GitHub...
    git push -u origin main
    
    if %errorlevel% neq 0 (
        echo.
        echo ⚠️  推送失败，可能是分支名称问题，尝试使用 master 分支...
        git branch -M master
        git push -u origin master
    )
) else (
    echo.
    echo 💡 提示：稍后手动执行以下命令推送到 GitHub
    echo   git remote add origin https://github.com/Cui-huo/REPO_NAME.git
    echo   git branch -M main
    echo   git push -u origin main
)

echo.
echo ========================================
echo ✅ 发布准备完成！
echo ========================================
pause
