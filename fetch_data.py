import requests
import pandas as pd

BINANCE_BASE_URL = "https://fapi.binance.com"
TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"]

def fetch_all_symbols():
    url = f"{BINANCE_BASE_URL}/fapi/v1/exchangeInfo"
    try:
        response = requests.get(url)
        data = response.json()
        symbols = [
            item["symbol"] for item in data["symbols"]
            if item["contractType"] == "PERPETUAL" and item["symbol"].endswith("USDT")
        ]
        return symbols
    except Exception as e:
        print(f"获取合约币种失败: {e}")
        return []

def get_symbol_data(symbol, interval, limit=150):
    url = f"{BINANCE_BASE_URL}/fapi/v1/klines"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])

        # 强制类型转换以防止部分字段为字符串
        df["timestamp"] = pd.to_numeric(df["open_time"], errors="coerce")
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df.dropna(subset=["timestamp", "close"], inplace=True)  # 删除无效数据行
        return df
    except Exception as e:
        print(f"获取K线失败：{symbol} - {interval} - {e}")
        return None

