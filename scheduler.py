import schedule
import time
from threading import Thread
from strategy_core import run_analysis
from config import DEFAULT_SYMBOLS, DEFAULT_RECEIVER
from wechat_notify import send_wechat

def job():
    for symbol in DEFAULT_SYMBOLS:
        try:
            result, _ = run_analysis(symbol)
            send_wechat(result, DEFAULT_RECEIVER)
        except Exception as e:
            print(f"❌ 定时任务运行出错：{e}")

def start_scheduler():
    schedule.every().day.at("10:00").do(job)
    print("✅ 定时任务已启动（每天10:00）")

    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    Thread(target=run_schedule, daemon=True).start()
