# app.py
from flask import Flask, request, render_template
from strategy_core import run_analysis
from wechat_notify import send_wechat_message

app = Flask(__name__)

# 主币种名单（只推送主币）
MAIN_COINS = ['BTC']

@app.route('/', methods=['GET', 'POST'])
def index():
    result_map = {}
    selected = []
    send_wechat = False

    if request.method == 'POST':
        selected = request.form.getlist('symbols')
        send_wechat = 'send_wechat' in request.form

        for symbol in selected:
            symbol = symbol.upper()
            result = run_analysis(symbol)
            result_map[symbol] = result

            if symbol in MAIN_COINS and send_wechat:
                send_wechat_message(f"小张每日研究 - {symbol}", result)

    return render_template('index.html',
                           symbols=['BTC', 'ETH', 'SOL', 'WLD'],
                           selected=selected,
                           send_wechat=send_wechat,
                           result_map=result_map)

if __name__ == '__main__':
    from scheduler import schedule_push_task
    schedule_push_task()

    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
