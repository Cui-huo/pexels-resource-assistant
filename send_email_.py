"""
send_email -
发邮件小脚本 SMTP

Author: 仗剑天涯
Date:2026/4/12

注意：邮箱配置从 download_and_send/config.py 导入，请勿硬编码
"""
import sys
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# 添加项目根目录到路径，以便导入 config
sys.path.insert(0, str(Path(__file__).parent / 'download_and_send'))
from config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, DEFAULT_RECEIVER

sender = EMAIL_SENDER
receivers = [DEFAULT_RECEIVER]  # 接收邮件，可设置为你的 QQ 邮箱或者其他邮箱

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = formataddr((str(Header('菜鸟教程', 'utf-8')), sender))
message['To'] = formataddr((str(Header('测试', 'utf-8')), receivers[0]))  # 接收者

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
    # 创建一个邮件对象 smtp（通过 host 和端口）
    smtpObj = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    # smtpObj = smtplib.SMTP('smtp.163.com', 25)
    # 调用登录方法，登录服务器，用户名和密钥（从 config.py 导入）
    smtpObj.login(sender, EMAIL_PASSWORD)
    # 调用发邮件方法，
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print(f"Error: 无法发送邮件 {e}")
