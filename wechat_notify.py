import requests
from config import WECHAT_KEYS

def send_wechat(content, receiver="默认通道"):
    key = WECHAT_KEYS.get(receiver)
    if not key:
        print(f"❌ 未找到微信接收人「{receiver}」的 Server酱 key")
        return

    url = f"https://sctapi.ftqq.com/{key}.send"
    data = {
        "title": "📊 小张每日研究",
        "desp": content
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✅ 微信通知发送成功")
        else:
            print(f"❌ 微信发送失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 微信推送异常: {e}")
