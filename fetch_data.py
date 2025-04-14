import requests
import pandas as pd

# 使用币安现货 API
BINANCE_SPOT_BASE_URL = "https://api.binance.com"

# 支持的时间周期
TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"]

def fetch_all_symbols():
    url = f"{BINANCE_SPOT_BASE_URL}/api/v3/exchangeInfo"
    try:
        response = requests.get(url)
        data = response.json()
        symbols = [
            s["symbol"] for s in data["symbols"]
            if s["status"] == "TRADING" and s["quoteAsset"] == "USDT"
        ]
        return symbols
    except Exception as e:
        print(f"获取现货交易对失败: {e}")
        return []

def get_symbol_data(symbol, interval, limit=150):
    full_symbol = symbol.upper() + "USDT"
    url = f"{BINANCE_SPOT_BASE_URL}/api/v3/klines"
    params = {"symbol": full_symbol, "interval": interval, "limit": limit}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 抛出 HTTP 错误（如 400）
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df["timestamp"] = pd.to_numeric(df["open_time"], errors="coerce")
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df.dropna(subset=["timestamp", "close"], inplace=True)
        return df
    except Exception as e:
        print(f"获取K线失败：{full_symbol} - {interval} - {e}")
        return None
