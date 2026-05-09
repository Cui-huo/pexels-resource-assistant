"""
send_email_.py - 邮件发送功能
可以发送带任意附件的邮件
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from urllib.parse import quote
from pathlib import Path
from config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, DEFAULT_RECEIVER

def create_attachment(filepath: Path, display_name: str = None) -> MIMEText:
    """把本地文件变成邮件附件对象"""
    if display_name is None:
        display_name = filepath.name
    with open(filepath, "rb") as f:
        att = MIMEText(f.read(), "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = f'attachment; filename="{quote(display_name)}"'
    return att

def send_email(subject: str, body: str, attachments: list = None, receiver: str = None):
    """
    发送邮件
    :param subject: 邮件主题
    :param body: 邮件正文（纯文本）
    :param attachments: 附件路径列表
    :param receiver: 收件人邮箱
    """
    if receiver is None:
        receiver = DEFAULT_RECEIVER

    msg = MIMEMultipart()
    msg["From"] = formataddr((str(Header("Pexels 小助手", "utf-8")), EMAIL_SENDER))
    msg["To"] = receiver
    msg["Subject"] = Header(subject, "utf-8")
    msg.attach(MIMEText(body, "plain", "utf-8"))

    if attachments:
        for filepath in attachments:
            if filepath.exists():
                msg.attach(create_attachment(filepath))
            else:
                print(f"⚠️ 附件不存在，跳过: {filepath}")

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ 邮件已发送至 {receiver}")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")