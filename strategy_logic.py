import pandas as pd
import pandas_ta as ta

def smart_contract_signal(df, tf):
    df = df.copy()
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["high"] = pd.to_numeric(df["high"], errors="coerce")
    df["low"] = pd.to_numeric(df["low"], errors="coerce")

    # 计算技术指标
    df["atr"] = ta.atr(high=df["high"], low=df["low"], close=df["close"], length=14)
    bb = ta.bbands(close=df["close"], length=20, std=2)
    df["bb_upper"] = bb["BBU_20_2.0"]
    df["bb_lower"] = bb["BBL_20_2.0"]

    macd = ta.macd(close=df["close"])
    df["macd"] = macd["MACD_12_26_9"]
    df["macd_signal"] = macd["MACDs_12_26_9"]

    latest = df.iloc[-1]
    atr = latest["atr"]
    close = latest["close"]
    macd_diff = latest["macd"] - latest["macd_signal"]

    prev_high = df["high"].iloc[-20:-1].max()
    prev_low = df["low"].iloc[-20:-1].min()

    # 默认方向为做多
    if macd_diff > 0 and close > latest["bb_upper"]:
        direction = "long"
        entry = close
        tp = entry + 2 * atr
        sl = prev_low
        reason = "MACD金叉，突破布林带上轨，趋势强劲"
    elif macd_diff < 0 and close < latest["bb_lower"]:
        direction = "short"
        entry = close
        tp = entry - 2 * atr
        sl = prev_high
        reason = "MACD死叉，跌破布林带下轨，趋势走弱"
    else:
        direction = "long" if macd_diff > 0 else "short"
        entry = close
        tp = entry + 1.5 * atr if direction == "long" else entry - 1.5 * atr
        sl = prev_low if direction == "long" else prev_high
        reason = "MACD轻微偏向 + 布林未破，结合ATR设置点位"

    return direction, round(entry, 4), round(tp, 4), round(sl, 4), reason


def generate_all_strategies(symbol, df):
    # 此处可以后续继续扩展五种风格的生成逻辑
    return {
        "策略": {
            "短期投机": {
                "建议持仓": "3小时",
                "解释": "结合K线结构、短期动能变化",
                "方向": "long",
                "入场": df["close"].iloc[-1],
                "目标": df["close"].iloc[-1] * 1.02,
                "止损": df["close"].iloc[-1] * 0.985,
                "止损比": "1.5%",
                "风险回报": "2.0"
            }
        }
    }
