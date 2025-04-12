# strategy_web_app/wechat_notify.py

import requests

SEND_KEY = "SCT276105TSPaSE9FuAyRT5rtjrGV9v7Zm"  # 你的 Server酱 SendKey

def send_wechat_message(title, content):
    url = f'https://sctapi.ftqq.com/{SEND_KEY}.send'
    data = {
        "title": title,
        "desp": content
    }
    try:
        resp = requests.post(url, data=data)
        if resp.status_code == 200:
            print("✅ 微信消息已发送")
        else:
            print(f"❌ 推送失败: {resp.text}")
    except Exception as e:
        print(f"[ERROR] 微信推送失败：{e}")
