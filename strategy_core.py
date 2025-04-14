import os
from fetch_data import get_symbol_data
from strategy_logic import generate_all_strategies, smart_contract_signal
from plot_kline_with_signals import plot_kline_with_signals
from simulation_utils import simulate_position
from config import DEFAULT_RECEIVER

FIVE_STYLE_TIMEFRAMES = ['1d']
ALL_CONTRACT_CYCLES = ['1m', '5m', '15m', '1h', '4h', '1d']
IMG_DIR = "static/charts"
os.makedirs(IMG_DIR, exist_ok=True)

def run_analysis(symbol):
    output = [f"📌 小张每日研究：{symbol}\n"]
    charts = {}

    # 策略建议
    output.append("🔄 策略根据大数据与AI分析建议")
    output.append("-" * 36)
    df_daily = get_symbol_data(symbol, '1d')
    if df_daily is not None and not df_daily.empty:
        strategies = generate_all_strategies(symbol, df_daily)
        for name, strat in strategies['策略'].items():
            output.append(f"{name}  建议持仓时间：{strat['建议持仓']}")
            output.append(f"信号解释: {strat['解释']}")
            output.append(f"方向: {'做多🟢' if strat['方向'] == 'long' else '做空🔴'}")
            output.append(f"📌 入场: {strat['入场']}")
            output.append(f"🌟 目标: {strat['目标']}")
            output.append(f"✂️ 止损: {strat['止损']} ({strat['止损比']})")
            output.append(f"风险回报: {strat['风险回报']} 🆗")
            output.append("-" * 36)
    else:
        output.append("【1d】获取日线数据失败 ❌")
        output.append("-" * 36)

    # 合约多空 + 仓位建议
    output.append("\n📌 合约策略速览（多空点位）")
    output.append("=" * 35)

    for tf in ALL_CONTRACT_CYCLES:
        df = get_symbol_data(symbol, tf)
        if df is None or df.empty:
            output.append(f"【{tf}】数据获取失败 ❌")
            continue

        direction, entry, tp, sl, reason = smart_contract_signal(df, tf)
        current = df['close'].iloc[-1]

        output.append(f"【{tf}】当前价格：{round(current, 2)}")
        output.append(f"{'🟢 做多' if direction == 'long' else '🔴 做空'}")
        output.append(f"理由：{reason}")
        output.append(f"入场 {entry}，止盈 {tp}，止损 {sl}")

        # 图表
        try:
            chart_path = plot_kline_with_signals(symbol, df.tail(30), tf, entry, tp, sl)
            if chart_path:
                output.append(f"<img src='/{chart_path}' style='width:100%; max-width:600px;'>")
                charts[tf] = chart_path
            else:
                output.append(f"【{tf}】图表生成失败 ❌")
        except Exception as e:
            output.append(f"【{tf}】图表生成出错：{e}")

        # 模拟仓位与AI建议
        sim_text = simulate_position(
            capital=1000,
            direction=direction,
            entry_price=entry,
            stop_price=sl,
            percent=0.2
        )
        output.append(sim_text)
        output.append("-" * 36)

    return "\n".join(output), charts
