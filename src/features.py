import pandas as pd
import pandas_ta as ta

def add_indicators(df: pd.DataFrame, ma_len=72, rsi_len=14, atr_len=14) -> pd.DataFrame:
    out = df.copy()
    out["MA"] = ta.sma(out["Close"], length=ma_len)
    out["RSI"] = ta.rsi(out["Close"], length=rsi_len)
    out["ATR"] = ta.atr(out["High"], out["Low"], out["Close"], length=atr_len)
    return out

def bullish_hammer(df: pd.DataFrame, lookback=1) -> bool:
    if df.empty or len(df) < lookback:
        return False
    row = df.iloc[-lookback]
    o, h, l, c = float(row["Open"]), float(row["High"]), float(row["Low"]), float(row["Close"])
    body = abs(c - o)
    rng = max(h - l, 1e-9)
    upper = h - max(o, c)
    lower = min(o, c) - l
    return (body / rng < 0.35) and (lower / rng > 0.55) and (upper / rng < 0.20)

