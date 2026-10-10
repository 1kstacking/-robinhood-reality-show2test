import streamlit as st
import json
import random

# Initial configuration JSON blueprint
if 'game_config' not in st.session_state:
    st.session_state.game_config = {
        "title": "Project Apollo: The Ultimate QC Reality Show",
        "episodes": [
            {"round": 1, "name": "The Smooth Opening", "chance": 0.15},
            {"round": 2, "name": "The Short Squeeze Twist", "chance": 0.60},
            {"round": 3, "name": "Flash Crash Mayhem", "chance": 0.85},
            {"round": 4, "name": "The Regulatory Crackdown", "chance": 0.40},
            {"round": 5, "name": "Grand Finale: Infinite Volatility", "chance": 0.95}
        ]
    }

# Initialize game states inside session storage memory
if 'round' not in st.session_state:
    st.session_state.round = 1
    st.session_state.health = 100
    st.session_state.quality_score = 100.0
    st.session_state.index_value = 1000.00
    st.session_state.game_over = False
    st.session_state.logs = ["🟢 Production pipeline initiated successfully."]
    st.session_state.anomaly_active = False

st.set_page_config(page_title="Project Apollo", layout="wide")
st.title("🎬 Project Apollo: The QC Reality Show Game")
st.caption("Deploying Quality Control Automation frameworks on Robinhood Index Portfolios.")

# Sidebar Metrics
st.sidebar.header("📊 Live Pipeline Metrics")
st.sidebar.metric("Pipeline Health", f"{st.session_state.health}%")
st.sidebar.progress(st.session_state.health / 100.0)

st.sidebar.metric("Quality Score", f"{st.session_state.quality_score}%")
st.sidebar.metric("Project Index Value", f"${st.session_state.index_value:,.2f}")

# Check game over conditions
if st.session_state.health <= 0 or st.session_state.quality_score < 40:
    st.session_state.game_over = True

if st.session_state.round > len(st.session_state.game_config["episodes"]):
    st.session_state.game_over = True

# Main Game Panel
if not st.session_state.game_over:
    current_episode = st.session_state.game_config["episodes"][st.session_state.round - 1]
    st.subheader(f"Episode {st.session_state.round}: {current_episode['name']}")
    
    # Trigger Event Step
    if st.button("🚀 Roll Market Conditions / Trigger Next Feed"):
        st.session_state.anomaly_active = random.random() < current_episode["chance"]
        if st.session_state.anomaly_active:
            st.session_state.logs.insert(0, f"⚠️ [ROUND {st.session_state.round}] TWIST: High volatility anomaly detected on ingestion stream!")
        else:
            st.session_state.logs.insert(0, f"✅ [ROUND {st.session_state.round}] Clean data stream verified. Ingestion normal.")
            # Normal calculation variance
            st.session_state.index_value *= random.uniform(0.98, 1.05)
            st.session_state.round += 1
            st.rerun()

    # Active Anomaly Decision Handling
    if st.session_state.anomaly_active:
        st.error("🚨 CRITICAL METRIC ALERT: QC-DATA-001 Fail! Packet streams show invalid Z-Score values.")
        st.write("Pick your mitigation strategy to survive the live broadcast:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛡️ DROP BAD PACKETS (Safe Integration)"):
                st.session_state.health -= 5
                st.session_state.quality_score = max(50.0, st.session_state.quality_score - 2.5)
                st.session_state.logs.insert(0, f"🟢 Mitigated Round {st.session_state.round}: Dropped bad packets. Math integrity saved.")
                st.session_state.anomaly_active = False
                st.session_state.round += 1
                st.rerun()
        with col2:
            if st.button("💥 PASS RAW DATA (Risk Ledger Contamination)"):
                st.session_state.health -= 35
                st.session_state.quality_score -= 25.0
                st.session_state.index_value *= random.uniform(0.55, 1.45)
                st.session_state.logs.insert(0, f"🔴 Failed Round {st.session_state.round}: Raw data flooded DB. Ledger data corrupted.")
                st.session_state.anomaly_active = False
                st.session_state.round += 1
                st.rerun()

else:
    st.header("🏁 Show Determination Results")
    if st.session_state.health <= 0 or st.session_state.quality_score < 40:
        st.error("❌ SYSTEM COLLAPSE: Your pipeline crashed on live television. The board has eliminated you.")
    else:
        st.success("🏆 CONGRATULATIONS! Your system survived the reality show grid. You win!")
        st.balloons()
    
    if st.button("🔄 Restart New Game Session"):
        st.session_state.clear()
        st.rerun()

# Operations Console Log View
st.subheader("🖥️ Operations Console Output Log")
for log in st.session_state.logs:
    st.text(log)
