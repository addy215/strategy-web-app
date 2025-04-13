from flask import Flask, request, render_template
from strategy_core import run_analysis
from wechat_notify import send_wechat_message

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    symbol = ""
    send_wechat = False

    if request.method == 'POST':
        symbol = request.form.get('symbol', '').upper()
        send_wechat = 'send_wechat' in request.form
        result = run_analysis(symbol)
        if send_wechat:
            send_wechat_message(f"小张每日研究 - {symbol}", result)

    return render_template('index.html',
                           result=result,
                           symbol=symbol,
                           send_wechat=send_wechat)

if __name__ == '__main__':
    from scheduler import schedule_push_task
    schedule_push_task()

    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
