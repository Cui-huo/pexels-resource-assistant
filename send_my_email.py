"""
send_my_email -
完成发邮件小脚本，
自主手打一遍，再自己写一个
学会创建邮件对象（2 种），其中一种可以添加附件
完成发送邮件的发送人、收件人信息格式化，
添加标题，正文，各种格式的附件
利用 smtp 对象学会创建对象，登录对象，发送信息

Author: 仗剑天涯
Date:2026/4/12

注意：邮箱配置从 download_and_send/config.py 导入，请勿硬编码
"""
import sys
from pathlib import Path
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from urllib.parse import quote

# 添加项目根目录到路径，以便导入 config
sys.path.insert(0, str(Path(__file__).parent / 'download_and_send'))
from config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, DEFAULT_RECEIVER

sender = EMAIL_SENDER     # 发送者从 config.py 导入
receivers = [DEFAULT_RECEIVER]   # 接收者从 config.py 导入
content = '月圆之夜，决战紫禁之巅'
content2 = """<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>"""
# 创建邮件对象法一
# email = MIMEText(content, 'plain', 'utf-8')
# email = MIMEText(content, 'html', 'utf-8')
# 创建邮件对象法二
email = MIMEMultipart('related')
email.attach(MIMEText(content))
# 创建发送者名字 + 地址的邮件显示规范
email['From'] = formataddr((str(Header('不死神皇', 'utf-8')), sender))
# 创建接受者名字 + 地址的邮件显示规范
email['To'] = formataddr((str(Header('无始大帝', 'utf-8')), receivers[0]))
# 邮件主题
email['Subject'] = Header('巅峰之战 9527')


# 创建 alternative 类型对象，
# 可选 html 和 TXT 文本展示方式给服务器
msgAlternative = MIMEMultipart('alternative')
# 文本对象添加进 related 类型（可以内嵌文本和图片）
email.attach(msgAlternative)
# HTML 正文
mail_msg = """
<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
<p>图片演示：</p>
<p><img src="cid:image1"></p>
"""
# 创建正文对象，并添加给可选正文对象
msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
# 指定图片为当前目录
fp = open('resources/888.png', 'rb')
# 创建图片对象
msgImage = MIMEImage(fp.read())
fp.close()
# 定义图片 ID，value 的值要和 HTML 中 cid 值相同
msgImage.add_header('Content-ID', '<image1>')
# 图片对象添加进可内嵌图片类型的邮件容器
email.attach(msgImage)



def creat_attachment(path, filename):
    _filename = filename
    _char = '/'
    if path == '':
        _char = ''
    with open(f'{path}{_char}{_filename}', 'rb') as foo:
        att2 = MIMEText(foo.read(), 'base64', 'utf-8')
        # 指定内容类型 - 附件。application/octet-stream：通用二进制流
        att2["Content-Type"] = 'application/octet-stream'
        # 如果函数有中文，需要处理成百分号编码 (
        # 收到邮件中显示百分号编码，但是下载到本地时，文件名会正确显示)
        _filename = quote(_filename)
        # 指定处理方式 - 下载
        att2["Content-Disposition"] = f'attachment; filename="{_filename}"'
        return att2

# 创建 xlsx 附件
email.attach(creat_attachment('', '一年级二班考试成绩表 2.xlsx'))
# 创建 docx 附件
email.attach(creat_attachment('', '离职证明 3.docx'))
# 创建 ppt 附件
email.attach(creat_attachment('resources', '演示 PPT.pptx'))
# 创建图片附件
email.attach(creat_attachment('resources', '888.png'))
# 创建视频附件
email.attach(creat_attachment('resources', 'pexels_video_1409899_Michal Marek.mp4'))


# 创建 smtp 对象，链接服务器和端口
smtp_obj = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
# smtp_obj = smtplib.SMTP('smtp.163.com', 25)
# 登录服务器（从 config.py 导入）
smtp_obj.login(sender, EMAIL_PASSWORD)
# 发送邮件
smtp_obj.sendmail(sender, receivers, email.as_string())
