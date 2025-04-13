from flask import Flask, request, render_template
from strategy_core import run_analysis, generate_chart_data
from wechat_notify import send_wechat_message
from email_notify import send_email

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    chart_data = None
    symbol = ""
    send_wechat = False
    send_email_flag = False
    wechat_key = ""

    if request.method == 'POST':
        symbol = request.form.get('symbol', '').upper()
        send_wechat = 'send_wechat' in request.form
        send_email_flag = 'send_email' in request.form
        wechat_key = request.form.get('wechat_key', '')

        result = run_analysis(symbol)
        chart_data = generate_chart_data(symbol)

        if send_wechat and wechat_key:
            send_wechat_message(f"小张每日研究 - {symbol}", result, key=wechat_key)

        if send_email_flag:
            send_email(f"小张每日研究 - {symbol}", result)

    return render_template('index.html',
                           result=result,
                           symbol=symbol,
                           send_wechat=send_wechat,
                           send_email=send_email_flag,
                           wechat_key=wechat_key,
                           chart_data=chart_data)

if __name__ == '__main__':
    from scheduler import schedule_push_task
    schedule_push_task()

    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
