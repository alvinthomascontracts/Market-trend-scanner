import streamlit as st
from src.scanner import scan_universe
from src.signals import under_ma_with_hammer, breakout_volume

st.set_page_config(layout="wide")
st.title("Market Trend Scanner (MVP)")
st.caption("Educational tool — not financial advice.")

default_watch = ["AAPL", "MSFT", "AMZN", "NVDA", "META", "TSLA", "GOOGL", "SPY"]
tickers_text = st.text_area("Universe tickers (comma-separated)", value=",".join(default_watch))
tickers = [x.strip().upper() for x in tickers_text.split(",") if x.strip()]

trend = st.selectbox("Trend template", [
    "Under MA + Bullish Hammer",
    "Breakout + Volume Spike",
])

colA, colB, colC = st.columns(3)
with colA:
    period = st.selectbox("Lookback period", ["3mo", "6mo", "1y", "2y"], index=1)
with colB:
    interval = st.selectbox("Interval", ["1d", "1h", "4h"], index=0)
with colC:
    limit = st.number_input("Max results", 10, 200, 50, 10)

st.subheader("Trend parameters")
if trend == "Under MA + Bullish Hammer":
    ma_len = st.slider("MA length", 20, 200, 72, 1)
    under_pct = st.slider("Under MA (%)", 0.5, 15.0, 3.0, 0.5)
    trend_fn = under_ma_with_hammer
    indicator_kwargs = {"ma_len": ma_len}
    trend_kwargs = {"ma_len": ma_len, "under_pct": under_pct}
else:
    lookback = st.slider("Breakout lookback (days)", 5, 100, 20, 1)
    vol_mult = st.slider("Volume multiple", 1.0, 5.0, 1.5, 0.1)
    trend_fn = breakout_volume
    indicator_kwargs = {}
    trend_kwargs = {"lookback": lookback, "vol_mult": vol_mult}

if st.button("Run scan"):
    with st.spinner("Scanning..."):
        results = scan_universe(
            tickers=tickers,
            trend_fn=trend_fn,
            period=period,
            interval=interval,
            indicator_kwargs=indicator_kwargs,
            trend_kwargs=trend_kwargs,
            limit=limit,
        )
    st.dataframe(results, use_container_width=True)
    st.download_button("Download CSV", results.to_csv(index=False), file_name="scan_results.csv")
