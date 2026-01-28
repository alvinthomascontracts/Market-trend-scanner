import pandas as pd
import streamlit as st
from .data import fetch_ohlcv
from .features import add_indicators

@st.cache_data(ttl=1800, max_entries=200)
def _cached_fetch(ticker: str, period: str, interval: str) -> pd.DataFrame:
    return fetch_ohlcv(ticker, period=period, interval=interval)

def scan_universe(
    tickers: list[str],
    trend_fn,
    period="6mo",
    interval="1d",
    indicator_kwargs=None,
    trend_kwargs=None,
    limit=50,
) -> pd.DataFrame:
    indicator_kwargs = indicator_kwargs or {}
    trend_kwargs = trend_kwargs or {}

    rows = []
    for t in tickers:
        df = _cached_fetch(t, period, interval)
        if df.empty:
            continue

        df = add_indicators(df, **indicator_kwargs)
        res = trend_fn(df, **trend_kwargs)

        last = df.iloc[-1]
close = last["Close"]
ma = last["MA"]

if isinstance(close, pd.Series): close = close.iloc[-1]
if isinstance(ma, pd.Series): ma = ma.iloc[-1]

rows.append({
    "Ticker": t,
    "Last": float(close) if pd.notna(close) else None,
    "MA": float(ma) if pd.notna(ma) else None,
,
            "ATR": float(last["ATR"]) if "ATR" in df.columns and pd.notna(last["ATR"]) else None,
            "Pass": bool(res["pass"]),
            "Score": float(res["score"]),
            "Notes": str(res["notes"]),
        })

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    return out.sort_values(["Pass", "Score"], ascending=[False, False]).head(limit)
