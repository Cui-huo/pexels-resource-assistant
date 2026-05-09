"""
send_email -
发邮件小脚本 SMTP

Author: 仗剑天涯
Date:2026/4/12

注意：邮箱配置从 .env 文件读取
"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

from utils.config_helper import get_email_config

# 获取邮箱配置
EMAIL_CONFIG = get_email_config()
sender = EMAIL_CONFIG['sender']
receivers = [EMAIL_CONFIG['default_receiver']]

# 创建邮件
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = formataddr((str(Header('菜鸟教程', 'utf-8')), sender))
message['To'] = formataddr((str(Header('测试', 'utf-8')), receivers[0]))
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
    # 创建 SMTP 对象并登录
    smtpObj = smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
    smtpObj.login(sender, EMAIL_CONFIG['password'])
    # 发送邮件
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print(f"Error: 无法发送邮件 {e}")
