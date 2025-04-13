from strategy_logic import generate_all_strategies, smart_contract_signal
from fetch_data import get_symbol_data

FIVE_STYLE_TIMEFRAMES = ['1m', '5m', '1h', '4h', '1d']
ALL_CONTRACT_CYCLES = ['1m', '5m', '15m', '1h', '4h', '1d']

def run_analysis(symbol):
    output = [f"、💸小张每日研究：{symbol}", "=" * 35]

    tf = '1d'
    df = get_symbol_data(symbol, tf)
    if df is None or df.empty:
        output.append(f"🕒 周期: {tf} 数据获取失败 ❌\n")
    else:
        result = generate_all_strategies(symbol, df)
        output.append(f"🕒 周期: {tf}")
        output.append(f"⛳ 当前价格: {result['当前价格']}")
        output.append("🔄 策略根据大数据与AI分析建议")
        output.append("------------------------------------")

        for name, strat in result['策略'].items():
            explanation = []
            if strat['原始信号'].get('MACD'):
                explanation.append("MACD出现金叉")
            if strat['原始信号'].get('RSI'):
                explanation.append("RSI反弹")
            if strat['RSI级别']:
                explanation.append(strat['RSI级别'])
            if strat['原始信号'].get('MA'):
                explanation.append("短期均线上穿长期均线")
            if strat.get('背离'):
                explanation.append(strat['背离'])

            signal_detail = "；".join(explanation) if explanation else "无明显信号"

            hold_time = {
                "超短线⚡": "几分钟到1小时",
                "短期投机🚀": "1小时到4小时",
                "小波段🌊": "4小时到1天",
                "波段🏄": "1天到3天",
                "长线🌳": "3天以上"
            }

            output.append(f"{name}  建议持仓时间：{hold_time[name]}")
            output.append(f"信号解释: {signal_detail}")
            output.append(f"方向: {strat['方向']}")
            output.append(f"📌 入场: {strat['入场']}")
            output.append(f"🌟 目标: {strat['目标']}")
            output.append(f"✂️ 止损: {strat['止损']} ({strat['止损比']})")
            output.append(f"风险回报: {strat['风险回报']} 🆗")
            output.append("------------------------------------")

    output.append("\n📌 合约策略速览（多空点位）")
    output.append("=" * 35)

    for tf in ALL_CONTRACT_CYCLES:
        df = get_symbol_data(symbol, tf)
        if df is None or df.empty:
            output.append(f"【{tf}】数据获取失败 ❌")
            continue

        direction, entry, tp, sl, reason = smart_contract_signal(df, tf)
        output.append(f"【{tf}】当前价格：{round(df['close'].iloc[-1], 3)}")
        output.append(f"{'🟢 做多' if direction == 'long' else '🔴 做空'}")
        output.append(f"理由：{reason}")
        output.append(f"入场 {entry}，止盈 {tp}，止损 {sl}")
        output.append("------------------------------------")

    return "\n".join(output)
