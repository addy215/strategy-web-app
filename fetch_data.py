# strategy_web_app/fetch_data.py

import ccxt
import pandas as pd

# 初始化现货市场
exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {
        'defaultType': 'spot'
    }
})

def get_symbol_data(symbol, timeframe='1h', limit=150):
    symbol = symbol.upper().strip()
    pair = f"{symbol}/USDT"

    try:
        markets = exchange.load_markets()

        if pair not in markets:
            print(f"[❌] Binance 不支持该交易对: {pair}")
            suggestions = [s for s in markets if symbol in s and '/USDT' in s]
            if suggestions:
                print(f"✅ 可选交易对: {suggestions[:5]}")
            return None

        ohlcv = exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    except Exception as e:
        print(f"[ERROR] 获取 {pair} 的数据失败：{e}")
        return None
