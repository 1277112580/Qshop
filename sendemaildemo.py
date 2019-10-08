import smtplib
from email.mime.text import MIMEText


# 构建邮件
# 主题
subject="网易云"

# 发送内容
content="小草偷偷地从土里钻出来，嫩嫩的，绿绿的。园子里，田野里，瞧去，一大片一大片满是的。坐着，躺着，打两个滚，踢几脚球，赛几趟跑，捉几回迷藏。风轻悄悄的，草软绵绵的。"
# 发送人
sender='gxy_hello@163.com'

# 接收人  单个 或多个收件人
rec="""gong.xiangyang@foxmail.com,
wyangyang95@163.com"""
password='qwe123'
# MIMEText 参数 发送内容 ，内容类型 编码
message=MIMEText(content,'plain','utf-8')
message['subject']=subject
message['From']=sender #发件人
message['To']=rec #收件人

# 发送邮件
smtp=smtplib.SMTP_SSL('smtp.163.com',465)
smtp.login(sender,password)
# 参数说明 发件人 收件人需要一个列表 发送邮件 类似一种json的格式
smtp.sendmail(sender,rec.split(",\n"),message.as_string())
smtp.close()
