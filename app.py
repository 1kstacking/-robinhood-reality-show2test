import streamlit as st
import json
import pandas as pd
import requests

st.set_page_config(page_title="Project Apollo Production Suite", layout="wide")
st.title("🛡️ Project Apollo: Enterprise Portfolio Index Control")

# 1. System Configuration Schema (Real-Use Matrix)
SYSTEM_CONFIG = {
    "index_name": "Robinhood Strategic Quality Index",
    "monitored_assets": ["HOOD", "AAPL", "NVDA", "MSFT"],
    "z_score_threshold": 3.0
}

# 2. Live Data Ingestion Engine
@st.cache_data(ttl=60) # Caches results for 60 seconds to comply with rate limits
def fetch_production_market_data(ticker):
    """Fetches real-time market data from a public API provider gateway"""
    url = f"https://yahoo.com{ticker}?interval=1m&range=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        meta = data["chart"]["result"]["meta"]
        current_price = meta["regularMarketPrice"]
        previous_close = meta["chartPreviousClose"]
        return {"price": current_price, "prev_close": previous_close, "status": "ONLINE"}
    except Exception as e:
        return {"price": None, "prev_close": None, "status": "OFFLINE"}

# 3. Running System State Initializer
if 'system_logs' not in st.session_state:
    st.session_state.system_logs = ["🟢 Operational Monitoring Framework Initiated Ready."]

# 4. Interface Metrics Dashboard
st.subheader("📊 Real-Time Production Asset Ledger")
asset_rows = []
pipeline_failures = 0

for ticker in SYSTEM_CONFIG["monitored_assets"]:
    ticker_data = fetch_production_market_data(ticker)
    
    if ticker_data["status"] == "ONLINE":
        # QC-DATA-001: Run Real Anomaly Detection Filter
        price_variance_pct = abs((ticker_data["price"] - ticker_data["prev_close"]) / ticker_data["prev_close"]) * 100
        
        # Flag anomalies if variance swings more than 10% inside a single day trading frame
        if price_variance_pct > 10.0:
            status_flag = "⚠️ ANOMALY DETECTED"
            pipeline_failures += 1
            st.session_state.system_logs.insert(0, f"❌ [QC-DATA-001 FAIL] Volatility breach detected on {ticker}: {price_variance_pct:.2f}% variance swing!")
        else:
            status_flag = "🟢 PASSED"
            
        asset_rows.append({
            "Asset": ticker,
            "Live Price ($)": f"{ticker_data['price']:.2f}",
            "Daily Variance (%)": f"{price_variance_pct:.2f}%",
            "QC Filter Status": status_flag
        })
    else:
        pipeline_failures += 1
        st.session_state.system_logs.insert(0, f"⚠️ [QC-DATA-002 FAIL] Data ingestion gap found for ticker {ticker}. Stream offline.")
        asset_rows.append({"Asset": ticker, "Live Price ($)": "N/A", "Daily Variance (%)": "N/A", "QC Filter Status": "🚨 STREAM OFFLINE"})

# Render Production Table Data
st.table(pd.DataFrame(asset_rows))

# Summary Metrics Panel
col1, col2 = st.columns(2)
with col1:
    health_pct = max(0, 100 - (pipeline_failures * 25))
    st.metric("Overall Operational Pipeline Health", f"{health_pct}%")
    st.progress(health_pct / 100.0)
with col2:
    st.metric("Active Tracked System Components", len(SYSTEM_CONFIG["monitored_assets"]))

# Live System Infrastructure Logging Readout
st.subheader("🖥️ Core System System Log Output")
for log in st.session_state.system_logs[:10]:
    st.text(log)
