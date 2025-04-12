# strategy_web_app/strategy_logic.py

import pandas as pd

# === 核心策略入口 ===
def generate_all_strategies(symbol, df):
    close = df['close']
    current = close.iloc[-1]

    macd_cross = check_macd_cross(close)
    rsi_sig, rsi_level = check_rsi(close)
    ma_cross = check_ma_cross(close)
    divergence = detect_divergence(df)

    raw_signals = {
        'MACD': macd_cross,
        'RSI': rsi_sig,
        'MA': ma_cross
    }

    strategies = {
        "超短线⚡": build_strategy(current, raw_signals, rsi_level, divergence, risk=0.015, reward=0.03),
        "短期投机🚀": build_strategy(current, raw_signals, rsi_level, divergence, risk=0.03, reward=0.05),
        "小波段🌊": build_strategy(current, raw_signals, rsi_level, divergence, risk=0.05, reward=0.1),
        "波段🏄": build_strategy(current, raw_signals, rsi_level, divergence, risk=0.1, reward=0.2, direction='short'),
        "长线🌳": build_strategy(current, raw_signals, rsi_level, divergence, risk=0.2, reward=0.4, direction='short')
    }

    return {
        "当前价格": round(current, 3),
        "策略": strategies
    }


def build_strategy(price, raw_signals, rsi_level, divergence, direction='long', risk=0.03, reward=0.05):
    entry = price * (0.99 if direction == 'long' else 1.01)
    target = entry * (1 + reward if direction == 'long' else 1 - reward)
    stop = entry * (1 - risk if direction == 'long' else 1 + risk)
    rr = abs((target - entry) / (entry - stop))
    stop_pct = round(abs((entry - stop) / entry) * 100, 2)

    return {
        "方向": "做多🟢" if direction == 'long' else "做空🔴",
        "入场": round(entry, 3),
        "目标": round(target, 3),
        "止损": round(stop, 3),
        "止损比": f"{stop_pct}%",
        "风险回报": round(rr, 2),
        "备注": " / ".join([k + "✅" for k, v in raw_signals.items() if v]) or "-",
        "原始信号": raw_signals,
        "背离": divergence,
        "RSI级别": rsi_level
    }


def recommend_direction(df):
    close = df['close']
    ma5 = close.rolling(5).mean()
    ma20 = close.rolling(20).mean()
    if ma5.iloc[-2] < ma20.iloc[-2] and ma5.iloc[-1] > ma20.iloc[-1]:
        return 'long'
    elif ma5.iloc[-2] > ma20.iloc[-2] and ma5.iloc[-1] < ma20.iloc[-1]:
        return 'short'
    return 'short'


def smart_contract_signal(df, tf='1h'):
    hold_map = {
        '1m': '建议持仓：几分钟',
        '5m': '建议持仓：10分钟到1小时',
        '15m': '建议持仓：30分钟到2小时',
        '1h': '建议持仓：1小时到4小时',
        '4h': '建议持仓：4小时到1天',
        '1d': '建议持仓：1天以上'
    }
    close = df['close']
    high = df['high']
    low = df['low']
    price = close.iloc[-1]

    ma5 = close.rolling(5).mean()
    ma20 = close.rolling(20).mean()
    ma_bull = ma5.iloc[-1] > ma20.iloc[-1]

    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / (avg_loss + 1e-6)
    rsi = 100 - (100 / (1 + rs))
    last_rsi = rsi.iloc[-1]

    recent_high = high.iloc[-20:].max()
    recent_low = low.iloc[-20:].min()
    volatility = (recent_high - recent_low) * 0.3
    min_stop = max(volatility, price * 0.005)

    if ma_bull and last_rsi < 70:
        reason = "均线多头排列"
        if last_rsi < 30:
            reason += " + RSI超卖"
        entry = round(price - min_stop * 0.5, 3)
        tp = round(price + min_stop * 2, 3)
        sl = round(price - min_stop, 3)
        return 'long', entry, tp, sl, reason + '；' + hold_map.get(tf, '')

    elif not ma_bull:
        reason = "均线空头排列"
        if last_rsi > 70:
            reason += " + RSI超买"
        entry = round(price + min_stop * 0.5, 3)
        tp = round(price - min_stop * 2, 3)
        sl = round(price + min_stop, 3)
        return 'short', entry, tp, sl, reason + '；' + hold_map.get(tf, '')

    reason = "无明显信号，倾向空"
    entry = round((recent_high + recent_low) / 2, 3)
    tp = round(recent_low, 3)
    sl = round(recent_high, 3)
    return 'short', entry, tp, sl, reason + '；' + hold_map.get(tf, '')


def check_macd_cross(close):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    hist = macd - signal
    return hist.iloc[-2] < 0 and hist.iloc[-1] > 0


def check_rsi(close, period=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / (avg_loss + 1e-6)
    rsi = 100 - (100 / (1 + rs))
    last_rsi = rsi.iloc[-1]
    label = None
    if last_rsi < 30:
        label = "RSI处于超卖区"
    elif last_rsi > 70:
        label = "RSI处于超买区"
    return last_rsi < 30 or last_rsi > 70, label


def check_ma_cross(close):
    ma5 = close.rolling(window=5).mean()
    ma20 = close.rolling(window=20).mean()
    return ma5.iloc[-2] < ma20.iloc[-2] and ma5.iloc[-1] > ma20.iloc[-1]


def detect_divergence(df):
    close = df['close']
    low = df['low']
    high = df['high']
    rsi = close.diff().apply(lambda x: x if x > 0 else 0).rolling(14).mean() / \
          close.diff().abs().rolling(14).mean() * 100

    if len(close) < 20:
        return None

    price_low = low.iloc[-5:].min()
    rsi_low = rsi.iloc[-5:].min()
    prev_price_low = low.iloc[-10:-5].min()
    prev_rsi_low = rsi.iloc[-10:-5].min()

    if price_low < prev_price_low and rsi_low > prev_rsi_low:
        return "出现底背离"

    price_high = high.iloc[-5:].max()
    rsi_high = rsi.iloc[-5:].max()
    prev_price_high = high.iloc[-10:-5].max()
    prev_rsi_high = rsi.iloc[-10:-5].max()

    if price_high > prev_price_high and rsi_high < prev_rsi_high:
        return "出现顶背离"

    return None