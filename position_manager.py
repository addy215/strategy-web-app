def calculate_liquidation_price(entry_price, leverage, direction='long', maintenance_margin_rate=0.004):
    """
    计算强平价格
    direction: 'long' or 'short'
    Binance默认维持保证金率大约为0.4%
    """
    if direction == 'long':
        liquidation_price = entry_price * (1 - 1 / leverage + maintenance_margin_rate)
    else:
        liquidation_price = entry_price * (1 + 1 / leverage - maintenance_margin_rate)
    return round(liquidation_price, 4)

def generate_position_advice(entry, tp, sl, capital=1000, direction='long'):
    """
    自动生成AI建议：建议仓位 + 加仓/减仓点 + 强平价格
    """
    risk_per_trade = 0.01  # 每次最大亏损 1%
    risk_amount = capital * risk_per_trade

    stop_loss_distance = abs(entry - sl)
    position_size = risk_amount / stop_loss_distance if stop_loss_distance != 0 else 0
    position_percent = min(position_size * entry / capital * 100, 100)

    # 仓位建议
    if position_percent < 10:
        advice = f"📌 仓位建议：轻仓试仓（建议使用 {round(position_percent, 1)}% 资金）"
    elif position_percent < 30:
        advice = f"📌 仓位建议：可适当加仓（建议使用 {round(position_percent, 1)}% 资金）"
    else:
        advice = f"📌 仓位建议：重仓需谨慎（建议使用 {round(position_percent, 1)}% 资金）"

    # 加减仓逻辑（本地模拟逻辑）
    add_point = entry + 0.5 * (tp - entry) if direction == 'long' else entry - 0.5 * (entry - tp)
    reduce_point = sl + 0.5 * (entry - sl) if direction == 'long' else sl - 0.5 * (sl - entry)

    advice += f"\n📈 加仓参考点：{round(add_point, 2)}"
    advice += f"\n📉 减仓参考点：{round(reduce_point, 2)}"

    # 强平价格
    liquidation_price = calculate_liquidation_price(entry, leverage=10, direction=direction)
    advice += f"\n🚨 强平参考价（10x杠杆）：{liquidation_price}"

    return advice
