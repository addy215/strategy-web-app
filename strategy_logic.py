def generate_all_strategies(symbol, df):
    # 简单逻辑示例，五种风格共用当前价格
    close = df['close'].iloc[-1]

    strategies = {
        "超短线⚡": {
            "建议持仓": "几分钟到1小时",
            "解释": "无明显信号",
            "方向": "做多🟢",
            "入场": round(close * 0.99, 3),
            "目标": round(close * 1.03, 3),
            "止损": round(close * 0.985, 3),
            "止损比": "1.5%",
            "风险回报": "2.0"
        },
        "短期投机🚀": {
            "建议持仓": "1小时到4小时",
            "解释": "无明显信号",
            "方向": "做多🟢",
            "入场": round(close * 0.99, 3),
            "目标": round(close * 1.05, 3),
            "止损": round(close * 0.96, 3),
            "止损比": "3.0%",
            "风险回报": "1.67"
        },
        "小波段🌊": {
            "建议持仓": "4小时到1天",
            "解释": "无明显信号",
            "方向": "做多🟢",
            "入场": round(close * 0.99, 3),
            "目标": round(close * 1.1, 3),
            "止损": round(close * 0.95, 3),
            "止损比": "5.0%",
            "风险回报": "2.0"
        },
        "波段🏄": {
            "建议持仓": "1天到3天",
            "解释": "无明显信号",
            "方向": "做空🔴",
            "入场": round(close * 1.01, 3),
            "目标": round(close * 0.8, 3),
            "止损": round(close * 1.1, 3),
            "止损比": "10.0%",
            "风险回报": "2.0"
        },
        "长线🌳": {
            "建议持仓": "3天以上",
            "解释": "无明显信号",
            "方向": "做空🔴",
            "入场": round(close * 1.01, 3),
            "目标": round(close * 0.6, 3),
            "止损": round(close * 1.2, 3),
            "止损比": "20.0%",
            "风险回报": "2.0"
        }
    }

    return {"策略": strategies}


def smart_contract_signal(df, tf):
    """
    简化版多空信号分析：根据均线判断
    """
    close = df['close']
    ma_short = close.rolling(window=5).mean()
    ma_long = close.rolling(window=20).mean()

    if ma_short.iloc[-1] > ma_long.iloc[-1]:
        direction = "long"
        entry = round(close.iloc[-1] * 0.995, 3)
        tp = round(close.iloc[-1] * 1.02, 3)
        sl = round(close.iloc[-1] * 0.985, 3)
        reason = "均线多头排列；建议持仓：" + time_frame_hold_time(tf)
    else:
        direction = "short"
        entry = round(close.iloc[-1] * 1.005, 3)
        tp = round(close.iloc[-1] * 0.98, 3)
        sl = round(close.iloc[-1] * 1.015, 3)
        reason = "均线空头排列；建议持仓：" + time_frame_hold_time(tf)

    return direction, entry, tp, sl, reason


def time_frame_hold_time(tf):
    mapping = {
        "1m": "几分钟",
        "5m": "10分钟到1小时",
        "15m": "30分钟到2小时",
        "1h": "1小时到4小时",
        "4h": "4小时到1天",
        "1d": "1天以上"
    }
    return mapping.get(tf, "未知周期")
