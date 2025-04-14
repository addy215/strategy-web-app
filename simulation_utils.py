def simulate_position(capital, direction, entry_price, stop_price, percent):
    """
    模拟仓位计算（不使用杠杆）
    :param capital: 总资金，如 1000（单位 USDT）
    :param direction: 'long' 或 'short'
    :param entry_price: 入场价格
    :param stop_price: 止损价格
    :param percent: 仓位百分比，例如 0.2 表示 20%
    :return: 建议文本
    """
    used_margin = capital * percent
    position_size = used_margin / entry_price
    if direction == "long":
        liquidation_price = entry_price - (used_margin / position_size)
    else:
        liquidation_price = entry_price + (used_margin / position_size)

    suggestions = [
        f"💡 仓位建议：使用{int(percent*100)}%仓位，即 {used_margin:.2f} USDT",
        f"🧮 仓位规模：{position_size:.4f} 张",
        f"⚠️ 强平价格预估：{liquidation_price:.2f}",
    ]

    if direction == "long":
        suggestions.append(f"📈 建议在价格上涨至 {entry_price*1.01:.2f} 加仓")
        suggestions.append(f"📉 跌至 {stop_price:.2f} 以下应考虑减仓或止损")
    else:
        suggestions.append(f"📉 建议在价格下跌至 {entry_price*0.99:.2f} 加仓")
        suggestions.append(f"📈 涨至 {stop_price:.2f} 以上应考虑减仓或止损")

    return "\n".join(suggestions)
