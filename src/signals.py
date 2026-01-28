import pandas as pd
from .features import bullish_hammer

def under_ma_with_hammer(df: pd.DataFrame, ma_len=72, under_pct=3.0) -> dict:
    if df.empty or "MA" not in df.columns:
        return {"pass": False, "score": 0.0, "notes": "No data/MA"}

    last = df.iloc[-1]
    if pd.isna(last["MA"]):
        return {"pass": False, "score": 0.0, "notes": "MA not ready"}

    close = float(last["Close"])
    ma = float(last["MA"])
    under = (ma - close) / ma * 100.0

    has_hammer = bullish_hammer(df, lookback=1)
    passed = (under >= under_pct) and has_hammer
    score = max(0.0, under) + (5.0 if has_hammer else 0.0)

    notes = f"Under MA: {under:.2f}% | Hammer: {has_hammer}"
    return {"pass": passed, "score": score, "notes": notes}

def breakout_volume(df: pd.DataFrame, lookback=20, vol_mult=1.5) -> dict:
    if df.empty or len(df) < lookback + 2:
        return {"pass": False, "score": 0.0, "notes": "Not enough data"}

    recent = df.tail(lookback + 1)
    prev_high = float(recent["High"].iloc[:-1].max())
    last = recent.iloc[-1]
    close = float(last["Close"])
    vol = float(last["Volume"])
    avg_vol = float(recent["Volume"].iloc[:-1].mean())

    passed = (close > prev_high) and (vol >= avg_vol * vol_mult)
    score = (close - prev_high) + (vol / max(avg_vol, 1e-9))
    notes = f"Close>prev{lookback}H: {close>prev_high} | Vol x: {vol/max(avg_vol,1e-9):.2f}"
    return {"pass": passed, "score": float(score), "notes": notes}
