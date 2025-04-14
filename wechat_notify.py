import requests
from config import WECHAT_KEYS

def send_wechat(content, receiver):
    """
    使用 Server 酱进行微信推送。
    参数：
        content: 推送的消息内容（字符串）
        receiver: 接收人名称，对应 config.py 中的 WECHAT_KEYS 键名
    """
    sckey = WECHAT_KEYS.get(receiver)
    if not sckey:
        print(f"❌ 未找到微信接收人「{receiver}」的 Server酱 key")
        return

    url = f"https://sctapi.ftqq.com/{sckey}.send"
    data = {
        "title": "📊 小张每日研究",
        "desp": content
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✅ 微信通知发送成功")
        else:
            print(f"❌ 微信通知发送失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"❌ 微信发送异常: {e}")
