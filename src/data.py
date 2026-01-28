import yfinance as yf
import pandas as pd

def fetch_ohlcv(ticker: str, period="6mo", interval="1d") -> pd.DataFrame:
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=False, progress=False)
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.rename(columns=str.title)
    df = df.reset_index()
    return df
