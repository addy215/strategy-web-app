import smtplib
from email.mime.text import MIMEText
from email.header import Header

SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SMTP_USER = "你的邮箱@qq.com"
SMTP_PASS = "你的授权码"

# 默认备用接收人（可选）
TO_LIST = ["备用@example.com"]

def send_email(subject, content, to=None):
    try:
        receivers = [to] if to else TO_LIST
        msg = MIMEText(content, "plain", "utf-8")
        msg["From"] = Header(SMTP_USER)
        msg["To"] = Header(",".join(receivers))
        msg["Subject"] = Header(subject, "utf-8")

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, receivers, msg.as_string())
        server.quit()
        print("📬 邮件发送成功")
    except Exception as e:
        print("❌ 邮件发送失败：", e)
