# strategy_web_app/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from strategy_core import run_analysis
from wechat_notify import send_wechat_message

def schedule_push_task():
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')

    # 每天早上 9:00 自动分析 SOL
    scheduler.add_job(func=lambda: send_wechat_message(
        "小张每日研究 - SOL (定时推送)",
        run_analysis("SOL")
    ), trigger='cron', hour=9, minute=0)

    scheduler.start()
    print("✅ 定时任务已启动（每天 9:00 推送）")
