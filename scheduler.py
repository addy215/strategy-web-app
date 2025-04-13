from apscheduler.schedulers.background import BackgroundScheduler
from strategy_core import run_analysis
from wechat_notify import send_wechat_message
import datetime
import pytz
import json
import os

CONFIG_FILE = "push_config.json"

def load_push_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def scheduled_task():
    print(f"\n🕒 执行定时分析任务 {datetime.datetime.now()}")

    config = load_push_config()
    for coin, setting in config.items():
        if setting.get("enabled"):
            print(f"📌 分析 {coin}，发送给：{setting.get('receiver')}")
            try:
                result = run_analysis(coin)
                send_wechat_message(f"小张每日研究 - {coin}", result, key=setting.get("receiver"))
            except Exception as e:
                print(f"❌ {coin} 分析或推送失败：{e}")

def schedule_push_task():
    scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Shanghai"))
    scheduler.add_job(scheduled_task, "cron", hour=10, minute=0)
    scheduler.start()
    print("✅ 定时任务已启动（每天10:00）")
