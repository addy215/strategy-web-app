def generate_strategy(df, tf):
    if df is None or df.empty:
        return {}
    close_price = float(df['close'].iloc[-1])
    direction = "多头" if tf in ["1m", "5m", "15m", "4h"] else "空头"
    return {
        "方向": direction,
        "入场": round(close_price, 2),
        "止盈": round(close_price * 1.02, 3),
        "止损": round(close_price * 0.98, 3),
        "仓位建议": "可适当加仓",
        "持仓周期": "短线" if tf in ["1m", "5m", "15m"] else "波段"
    }
