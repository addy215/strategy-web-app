import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 修改你的邮箱配置
SMTP_SERVER = "smtp.qq.com"            # SMTP服务器（QQ邮箱）
SMTP_PORT = 465                        # 通常是465（SSL）
SMTP_USER = "你的邮箱@qq.com"
SMTP_PASS = "你的授权码"

TO_LIST = [
    "接收者1@example.com",
    "接收者2@example.com"
]

def send_email(subject, content):
    try:
        msg = MIMEText(content, "plain", "utf-8")
        msg["From"] = Header(SMTP_USER)
        msg["To"] = Header(",".join(TO_LIST))
        msg["Subject"] = Header(subject, "utf-8")

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, TO_LIST, msg.as_string())
        server.quit()
        print("📬 邮件发送成功")
    except Exception as e:
        print("❌ 邮件发送失败：", e)
