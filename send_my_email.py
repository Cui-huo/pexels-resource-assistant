"""
send_my_email - 
完成发邮件小脚本，
自主手打一遍，再自己写一个
学会创建邮件对象（2种），其中一种可以添加附件
完成发送邮件的发送人、收件人信息格式化，
添加标题，正文，各种格式的附件
利用smtp对象学会创建对象，登录对象，发送信息
脚本代码逻辑结构图：

multipart/related  （最外层，可内嵌图片和文本）
├── multipart/alternative  （容器，封装正文的不同版本）
│   ├── text/plain  （纯文本版本，可选）
│   └── text/html   （HTML 版本，其中用 cid:xxx 引用图片）
└── image/png  （内嵌图片，Content-ID 与 HTML 中的 cid 匹配）
Author:仗剑天涯
Date:2026/4/12
"""
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from urllib.parse import quote


sender = 'heiye_duxing@163.com'     # 发送者
receivers = ['1414829065@qq.com']   # 接收者
content = '月圆之夜，决战紫禁之巅'
content2 = """<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>"""
# 创建邮件对象法一
# email = MIMEText(content, 'plain', 'utf-8')
# email = MIMEText(content, 'html', 'utf-8')
# 创建邮件对象法二
email = MIMEMultipart('related')
email.attach(MIMEText(content))
# 创建发送者名字+地址的邮件显示规范
email['From'] = formataddr((str(Header('不死神皇', 'utf-8')), sender))
# 创建接受者名字+地址的邮件显示规范
email['To'] = formataddr((str(Header('无始大帝', 'utf-8')), receivers[0]))
# 邮件主题
email['Subject'] = Header('巅峰之战9527')


# 创建alternative类型对象，
# 可选html和TXT文本展示方式给服务器
msgAlternative = MIMEMultipart('alternative')
# 文本对象添加进related类型（可以内嵌文本和图片）
email.attach(msgAlternative)
# HTML正文
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
# 定义图片 ID，value的值要和HTML中cid值相同
msgImage.add_header('Content-ID', '<image1>')
# 图片对象添加进可内嵌图片类型的邮件容器
email.attach(msgImage)



"""附件发送部分

# 构造第一个附件，读取当前目录下的 test.txt 文件
# MIMEText 用于创建 MIME 文本对象，但这里巧妙地将二进制文件内容用 base64 编码后当作文本处理
att1 = MIMEText(open('test.txt', 'rb').read(), 'base64', 'utf-8')
# 设置附件的 Content-Type 为 application/octet-stream，表示这是一个通用的二进制数据流（即附件）
att1["Content-Type"] = 'application/octet-stream'
# 设置 Content-Disposition 为 attachment，并指定文件名（邮件中显示的名称）
# filename 可以任意写，与实际文件名无关
att1["Content-Disposition"] = 'attachment; filename="test.txt"'
# 将该附件对象添加到邮件对象 message 中
email.attach(att1)

# 构造第二个附件
# att2 = MIMEText(open('test.txt', 'rb').read(), 'base64', 'utf-8')
with open('一年级二班考试成绩表.xls', 'rb') as foo:
    att2 = MIMEText(foo.read(), 'base64', 'utf-8')
    # 指定内容类型-附件
    att2["Content-Type"] = 'application/octet-stream'
    # 如果函数有中文，需要处理成百分号编码(
    # 收到邮件中显示百分号编码，但是下载到本地时，文件名会正确显示)
    filename = quote('成绩表.xls')
    # 指定处理方式-下载
    att2["Content-Disposition"] = f'attachment; filename="{filename}"'
    email.attach(att2)"""


def creat_attachment(path, filename):
    _filename = filename
    _char = '/'
    if path == '':
        _char = ''
    with open(f'{path}{_char}{_filename}', 'rb') as foo:
        att2 = MIMEText(foo.read(), 'base64', 'utf-8')
        # 指定内容类型-附件。application/octet-stream：通用二进制流
        att2["Content-Type"] = 'application/octet-stream'
        # 如果函数有中文，需要处理成百分号编码(
        # 收到邮件中显示百分号编码，但是下载到本地时，文件名会正确显示)
        _filename = quote(_filename)
        # 指定处理方式-下载
        att2["Content-Disposition"] = f'attachment; filename="{_filename}"'
        return att2

# 创建xlsx附件
email.attach(creat_attachment('', '一年级二班考试成绩表 2.xlsx'))
# 创建docx附件
email.attach(creat_attachment('', '离职证明3.docx'))
# 创建ppt附件
email.attach(creat_attachment('resources', '演示PPT.pptx'))
# 创建图片附件
email.attach(creat_attachment('resources', '888.png'))
# 创建视频附件
email.attach(creat_attachment('resources', 'pexels_video_1409899_Michal Marek.mp4'))


# 创建smtp对象，链接服务器和端口
smtp_obj = smtplib.SMTP_SSL('smtp.163.com', 465)
# smtp_obj = smtplib.SMTP('smtp.163.com', 25)
# 登录服务器
smtp_obj.login('heiye_duxing@163.com', 'NPbLvKNgZzydDrHb')
# 发送邮件
smtp_obj.sendmail(sender, receivers, email.as_string())
