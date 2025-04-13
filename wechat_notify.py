import requests

# ✅ 这是默认备用的 key（可选）
DEFAULT_WECHAT_KEY = "SCT00000DEFAULTKEY"

def send_wechat_message(title, content, key=None):
    """
    发送微信消息：
    - key: Server酱的 key（网页传入）
    - 若未提供 key，将使用默认值
    """
    use_key = key or DEFAULT_WECHAT_KEY
    url = f"https://sctapi.ftqq.com/{use_key}.send"

    try:
        resp = requests.post(url, data={"title": title, "desp": content})
        if resp.status_code == 200:
            print(f"✅ 微信推送成功（Key: {use_key}）")
        else:
            print(f"❌ 推送失败：{resp.status_code}, {resp.text}")
    except Exception as e:
        print(f"❌ 推送异常：{e}")
