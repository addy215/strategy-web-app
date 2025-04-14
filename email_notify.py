import smtplib
from email.mime.text import MIMEText
from email.header import Header

SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "461548470@qq.com"
SMTP_AUTH_CODE = "bpboyynhcsanbjci"

def send_email(to_address, symbol, content):
    try:
        msg = MIMEText(content, "plain", "utf-8")
        subject = f"小张每日研究：{symbol} 分析报告"
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_address

        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, SMTP_AUTH_CODE)
        smtp.sendmail(EMAIL_ADDRESS, to_address, msg.as_string())
        smtp.quit()
        print(f"✅ 邮件已发送至 {to_address}")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
