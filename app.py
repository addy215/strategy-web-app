from flask import Flask, request, render_template, redirect, url_for
from strategy_core import run_analysis, generate_chart_data
from wechat_notify import send_wechat_message
from email_notify import send_email
from scheduler import schedule_push_task
import os, json

app = Flask(__name__)

PUSH_CONFIG_FILE = "push_config.json"
DEFAULT_RECEIVER = "SCT276105TSPaSE9FuAyRT5rtjrGV9v7Zm"

def load_push_config():
    coins = ['BTC', 'ETH', 'SOL', 'WLD']
    config = {coin: {"enabled": False, "receiver": DEFAULT_RECEIVER} for coin in coins}
    if os.path.exists(PUSH_CONFIG_FILE):
        with open(PUSH_CONFIG_FILE, 'r', encoding='utf-8') as f:
            saved = json.load(f)
            config.update(saved)
    return config

def save_push_config(config):
    with open(PUSH_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    chart_data = None
    symbol = ""
    send_wechat = False
    send_email_flag = False
    wechat_key = ""
    email_address = ""

    if request.method == 'POST':
        symbol = request.form.get('symbol', '').upper()
        send_wechat = 'send_wechat' in request.form
        send_email_flag = 'send_email' in request.form
        wechat_key = request.form.get('wechat_key', '')
        email_address = request.form.get('email_address', '')

        result = run_analysis(symbol)
        chart_data = generate_chart_data(symbol)

        if send_wechat and wechat_key:
            send_wechat_message(f"小张每日研究 - {symbol}", result, key=wechat_key)

        if send_email_flag and email_address:
            send_email(f"小张每日研究 - {symbol}", result, to=email_address)

    return render_template('index.html',
                           result=result,
                           symbol=symbol,
                           send_wechat=send_wechat,
                           send_email=send_email_flag,
                           wechat_key=wechat_key,
                           email_address=email_address,
                           chart_data=chart_data)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    config = load_push_config()
    coins = config.keys()

    if request.method == 'POST':
        for coin in coins:
            enabled = f'enabled_{coin}' in request.form
            receiver = request.form.get(f'receiver_{coin}', '')
            config[coin] = {
                "enabled": enabled,
                "receiver": receiver or DEFAULT_RECEIVER
            }
        save_push_config(config)
        return redirect(url_for('schedule'))

    return render_template('schedule.html', config=config)

if __name__ == '__main__':
    schedule_push_task()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
