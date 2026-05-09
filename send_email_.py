"""
send_email - 
发邮件小脚本SMTP

Author:仗剑天涯
Date:2026/4/12
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

sender = 'heiye_duxing@163.com'
receivers = ['1414829065@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = formataddr((str(Header('菜鸟教程', 'utf-8')), sender))
message['To'] = formataddr((str(Header('测试', 'utf-8')), receivers[0]))  # 接收者

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
    # 创建一个邮件对象smtp（通过host和端口）
    smtpObj = smtplib.SMTP_SSL('smtp.163.com', 465)
    # smtpObj = smtplib.SMTP('smtp.163.com', 25)
    # 调用登录方法，登录服务器，用户名和密钥
    smtpObj.login('heiye_duxing@163.com', 'NPbLvKNgZzydDrHb')
    # 调用发邮件方法，
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")


"""email = MIMEMultipart()
email['From'] = formataddr((str(Header('帝尊', 'utf-8')), 'heiye_duxing@163.com'))
email['To'] = formataddr((str(Header('狠人大帝', 'utf-8')), '1414829065@qq.com'))
# email['From'] = Header('帝尊', 'utf-8')
# email['To'] = Header('狠人大帝', 'utf-8')
email['Subject'] = Header('谈恋爱高手在线教我谈恋爱', 'utf-8')
content = "她的潜台词可能是：“我不喜欢为了吃而特意跑出去，太折腾。”
“我可能比较宅，不喜欢这种形式的约会。”“我不想让‘吃饭’成为我们互动的主题。”
但注意：她没有说“我不想见你”，也没有说“我不想跟你聊了”。 她只
是拒绝了一种活动形式。这是好事，因为她给了你信息，而不是直接消失。"

email.attach(MIMEText(content, 'plain'))
sender = 'heiye_duxing@163.com'
receivers = '1414829065@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

smtp_obj = smtplib.SMTP_SSL('smtp.163.com', 465)
# smtp_obj.connect('smtp.163.com', 465)
smtp_obj.login('heiye_duxing@163.com', 'NPbLvKNgZzydDrHb')
smtp_obj.sendmail(sender, receivers, email.as_string())
smtp_obj.quit()"""