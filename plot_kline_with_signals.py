import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
import pandas as pd
import time

# 自动找中文字体，避免乱码
font_paths = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
zh_font = None
for font_path in font_paths:
    if any(kw in font_path.lower() for kw in ['simhei', 'msyh', 'noto', 'simsun']):
        zh_font = font_path
        break
if zh_font:
    plt.rcParams['font.family'] = font_manager.FontProperties(fname=zh_font).get_name()

IMG_DIR = "static/charts"
os.makedirs(IMG_DIR, exist_ok=True)

def plot_kline_with_signals(symbol, df, tf, entry, tp, sl):
    df = df.copy()

    # 确保存在 timestamp 列
    if "timestamp" not in df.columns:
        if "open_time" in df.columns:
            df["timestamp"] = pd.to_datetime(df["open_time"], unit="ms")
        else:
            df["timestamp"] = pd.to_datetime(df.index)

    # 保证 timestamp 是 datetime 类型
    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    # 如果 timestamp 是整数（即毫秒），需转换为 datetime
    if pd.api.types.is_integer_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # 设置索引并转换时区
    df.set_index("timestamp", inplace=True)

    # 绘制图表
    plt.figure(figsize=(7, 3))
    plt.plot(df.index, df["close"], label="价格", linewidth=1.5)
    if entry: plt.axhline(entry, color="blue", linestyle="--", label=f"入场: {entry}")
    if tp: plt.axhline(tp, color="green", linestyle="--", label=f"止盈: {tp}")
    if sl: plt.axhline(sl, color="red", linestyle="--", label=f"止损: {sl}")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M", tz=df.index.tz))
    plt.xticks(rotation=45)
    plt.title(f"{symbol.upper()} {tf} K线图（东京时间）")
    plt.legend(loc="upper left")
    plt.tight_layout()

    filename = f"{symbol}_{tf}_{int(time.time())}.png"
    filepath = os.path.join(IMG_DIR, filename)
    plt.savefig(filepath)
    plt.close()
    return filepath.replace("\\", "/")
