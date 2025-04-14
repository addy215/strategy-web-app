import math

def calculate_liquidation_price(entry_price, leverage, is_long=True):
    try:
        entry_price = float(entry_price)
        leverage = float(leverage)
        if leverage <= 0:
            return "无效杠杆"
        if is_long:
            return round(entry_price * (1 - 1 / leverage), 4)
        else:
            return round(entry_price * (1 + 1 / leverage), 4)
    except:
        return "计算失败"

def generate_position_suggestion(entry, tp, sl):
    try:
        entry = float(entry)
        tp = float(tp)
        sl = float(sl)
        risk = abs(entry - sl)
        reward = abs(tp - entry)
        if risk == 0:
            return "⚠️ 止损为0，无法评估"
        rr_ratio = reward / risk
        if rr_ratio > 2.0:
            return "✅ 建议重仓（风险回报 {:.2f}）".format(rr_ratio)
        elif rr_ratio > 1.5:
            return "✅ 建议适当加仓（风险回报 {:.2f}）".format(rr_ratio)
        elif rr_ratio > 1.0:
            return "✅ 建议轻仓试单（风险回报 {:.2f}）".format(rr_ratio)
        else:
            return "⚠️ 建议观望（风险回报 {:.2f}）".format(rr_ratio)
    except:
        return "⚠️ 建议生成失败"

def add_position_management_module(entry, tp, sl, leverage=10, is_long=True):
    suggestion = generate_position_suggestion(entry, tp, sl)
    liquidation = calculate_liquidation_price(entry, leverage, is_long)

    result = [
        "📊 智能仓位建议模块",
        f"🪙 杠杆倍数：{leverage}x",
        f"💡 {suggestion}",
        f"💣 估算强平价格：{liquidation}"
    ]

    try:
        entry = float(entry)
        tp = float(tp)
        if is_long:
            result.append(f"➕ 建议在 {round(entry * 0.99, 4)} 加仓")
            result.append
