import pandas as pd
from .features import bullish_hammer

def _to_scalar(x):
    """Convert pandas/numpy scalars or 1-element Series to python scalar."""
    if isinstance(x, pd.Series):
        # If multiple values, take the last (most recent)
        x = x.iloc[-1]
    return x

def under_ma_with_hammer(df: pd.DataFrame, ma_len=72, under_pct=3.0) -> dict:
    if df.empty or "MA" not in df.columns:
        return {"pass": False, "score": 0.0, "notes": "No data/MA"}

    last = df.iloc[-1]

    ma_val = _to_scalar(last.get("MA"))
    close_val = _to_scalar(last.get("Close"))

    if ma_val is None or pd.isna(ma_val):
        return {"pass": False, "score": 0.0, "notes": "MA not ready"}

    try:
        close = float(close_val)
        ma = float(ma_val)
    except Exception:
        return {"pass": False, "score": 0.0, "notes": "Bad numeric values"}

    under = (ma - close) / ma * 100.0

    has_hammer = bullish_hammer(df, lookback=1)
    passed = (under >= under_pct) and has_hammer
    score = max(0.0, under) + (5.0 if has_hammer else 0.0)

    notes = f"Under MA: {under:.2f}% | Hammer: {has_hammer}"
    return {"pass": passed, "score": score, "notes": notes}
