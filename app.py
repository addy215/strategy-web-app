from flask import Flask, render_template, request
from strategy_core import run_analysis
from config import DEFAULT_SYMBOLS, DEFAULT_RECEIVER, WECHAT_KEYS
from wechat_notify import send_wechat

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    charts = []
    if request.method == "POST":
        symbol = request.form.get("symbol", "").upper()
        receiver = request.form.get("receiver", DEFAULT_RECEIVER)

        if symbol:
            try:
                result, charts = run_analysis(symbol)
                send_wechat(result, receiver)
            except Exception as e:
                result = f"❌ 分析过程中出错: {e}"

    return render_template("index.html",
                           result=result,
                           charts=charts,
                           default_symbols=DEFAULT_SYMBOLS,
                           wechat_keys=WECHAT_KEYS,
                           default_receiver=DEFAULT_RECEIVER)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
