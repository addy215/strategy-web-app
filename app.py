from flask import Flask, request, render_template_string
from strategy_core import run_analysis
from wechat_notify import send_wechat_message

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>小张每日研究</title>
<h2>输入币种（如 BTC 或 SOL）</h2>
<form method="post">
  <input name="symbol" value="{{ symbol }}" autofocus required>
  <label>
    <input type="checkbox" name="send_wechat" {% if send_wechat %}checked{% endif %}>
    推送结果到微信
  </label>
  <br><br>
  <input type="submit" value="分析">
</form>
{% if result %}
<hr>
<pre>{{ result }}</pre>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    symbol = ''
    result = ''
    send_wechat = False

    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
        result = run_analysis(symbol)
        send_wechat = 'send_wechat' in request.form

        if send_wechat:
            send_wechat_message(f"小张每日研究 - {symbol}", result)

    return render_template_string(
        HTML_TEMPLATE,
        symbol=symbol,
        result=result,
        send_wechat=send_wechat
    )

if __name__ == '__main__':
    # ✅ 启动定时任务（每天 9:00 推送 SOL）
    from scheduler import schedule_push_task
    schedule_push_task()

    app.run(debug=True)
