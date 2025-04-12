import ccxt

exchange = ccxt.binance()
markets = exchange.load_markets()

symbol = "SOL/USDT"

if symbol in markets:
    print(f"✅ 找到现货交易对: {symbol}")
    data = exchange.fetch_ohlcv(symbol, timeframe="1h", limit=5)
    for entry in data:
        print(entry)
else:
    print(f"❌ 没有找到 {symbol}")
