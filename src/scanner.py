import pandas as pd
import streamlit as st
from .data import fetch_ohlcv
from .features import add_indicators

@st.cache_data(ttl=1800, max_entries=200)
def _cached_fetch(ticker: str, period: str, interval: str) -> pd.DataFrame:
    return fetch_ohlcv(ticker, period=period, interval=interval)

def _scalar(x):
    # yfinance/pandas can sometimes return a 1-element Series; make it a scalar
    if isinstance(x, pd.Series):
        return x.iloc[-1]
    return x

def scan_universe(
    tickers,
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
        if df is None or df.empty:
            continue

        df = add_indicators(df, **indicator_kwargs)
        res = trend_fn(df, **trend_kwargs)

        last = df.iloc[-1]
        close = _scalar(last.get("Close"))
        ma = _scalar(last.get("MA"))
        atr = _scalar(last.get("ATR")) if "ATR" in df.columns else None

        rows.append(
            {
                "Ticker": str(t),
                "Last": float(close) if pd.notna(close) else None,
                "MA": float(ma) if pd.notna(ma) else None,
                "ATR": float(atr) if atr is not None and pd.notna(atr) else None,
                "Pass": bool(res.get("pass", False)),
                "Score": float(res.get("score", 0.0)),
                "Notes": str(res.get("notes", "")),
            }
        )

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    return out.sort_values(["Pass", "Score"], ascending=[False, False]).head(int(limit))
