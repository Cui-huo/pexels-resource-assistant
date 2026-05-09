"""
send_my_email -
完成发邮件小脚本，
自主手打一遍，再自己写一个

Author: 仗剑天涯
Date:2026/4/12

注意：邮箱配置从 .env 文件读取
"""
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from urllib.parse import quote

from utils.config_helper import get_email_config

# 获取邮箱配置
EMAIL_CONFIG = get_email_config()
sender = EMAIL_CONFIG['sender']
receivers = [EMAIL_CONFIG['default_receiver']]
content = '月圆之夜，决战紫禁之巅'

# 创建邮件对象
email = MIMEMultipart('related')
email.attach(MIMEText(content))
email['From'] = formataddr((str(Header('不死神皇', 'utf-8')), sender))
email['To'] = formataddr((str(Header('无始大帝', 'utf-8')), receivers[0]))
email['Subject'] = Header('巅峰之战 9527')

# 创建 alternative 类型对象
msgAlternative = MIMEMultipart('alternative')
email.attach(msgAlternative)
mail_msg = """
<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">菜鸟教程链接</a></p>
<p>图片演示：</p>
<p><img src="cid:image1"></p>
"""
msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

fp = open('resources/888.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
msgImage.add_header('Content-ID', '<image1>')
email.attach(msgImage)


def creat_attachment(path, filename):
    _filename = filename
    _char = '/'
    if path == '':
        _char = ''
    with open(f'{path}{_char}{_filename}', 'rb') as foo:
        att2 = MIMEText(foo.read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        _filename = quote(_filename)
        att2["Content-Disposition"] = f'attachment; filename="{_filename}"'
        return att2

# 创建附件
email.attach(creat_attachment('', '一年级二班考试成绩表 2.xlsx'))
email.attach(creat_attachment('', '离职证明 3.docx'))
email.attach(creat_attachment('resources', '演示 PPT.pptx'))
email.attach(creat_attachment('resources', '888.png'))
email.attach(creat_attachment('resources', 'pexels_video_1409899_Michal Marek.mp4'))

# 发送邮件
smtp_obj = smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
smtp_obj.login(sender, EMAIL_CONFIG['password'])
smtp_obj.sendmail(sender, receivers, email.as_string())
