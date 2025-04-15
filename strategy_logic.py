import pandas as pd
import pandas_ta as ta

def smart_contract_signal(df, tf):
    df = df.copy()
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df.dropna(inplace=True)

    # 计算指标
    atr = ta.atr(df["high"], df["low"], df["close"], length=14)
    macd = ta.macd(df["close"])
    bb = ta.bbands(df["close"], length=20)

    # 默认方向判断（简单示例）
    direction = "long" if macd["MACD_12_26_9"].iloc[-1] > 0 else "short"

    # 计算止盈止损点位
    current_price = df["close"].iloc[-1]
    atr_value = atr.iloc[-1]
    stop_offset = atr_value * (2 if tf in ["1d", "4h"] else 1.5)
    tp_offset = atr_value * (3 if tf in ["1d", "4h"] else 2)

    if direction == "long":
        entry = current_price
        stop = entry - stop_offset
        tp = entry + tp_offset
    else:
        entry = current_price
        stop = entry + stop_offset
        tp = entry - tp_offset

    reason = f"基于MACD与ATR（{round(atr_value, 2)}）计算，方向：{direction}"
    return direction, round(entry, 4), round(tp, 4), round(stop, 4), reason
