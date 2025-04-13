from apscheduler.schedulers.background import BackgroundScheduler
from strategy_core import run_analysis
from wechat_notify import send_wechat_message
from config_push import SCHEDULED_PUSH_LIST
import datetime
import pytz

def scheduled_task():
    print(f"\n🕒 执行定时分析任务 {datetime.datetime.now()}")

    for item in SCHEDULED_PUSH_LIST:
        symbol = item['symbol']
        key = item['wechat_key']
        print(f"📌 正在分析 {symbol}，并准备推送到微信")

        try:
            result = run_analysis(symbol)
            send_wechat_message(f"小张每日研究 - {symbol}", result, key=key)
        except Exception as e:
            print(f"❌ 分析或推送失败（{symbol}）：{e}")

def schedule_push_task():
    scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Shanghai'))

    # 每天早上 10 点执行定时任务
    scheduler.add_job(scheduled_task, 'cron', hour=10, minute=0)
    scheduler.start()
    print("✅ 定时任务已启动（每天10:00分析并推送）")
