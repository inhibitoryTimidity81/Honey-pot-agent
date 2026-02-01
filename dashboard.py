import streamlit as st
import pandas as pd
import json
import sqlite3
import os
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Honeypot Live Intel", layout="wide", page_icon="🕵️")

# Force Absolute Path for DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "honeypot_logs.db")

# --- CUSTOM CSS FOR WHATSAPP LOOK ---
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage[data-testid="chat-message-user"] {
        background-color: #3b1e1e;
        border-left: 5px solid #ff4b4b;
    }
    .stChatMessage[data-testid="chat-message-assistant"] {
        background-color: #1e3b26;
        border-left: 5px solid #00c853;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNCTIONS ---
def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM sessions ORDER BY last_update DESC", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def calculate_duration(start_str, end_str):
    try:
        fmt = "%Y-%m-%d %H:%M:%S"
        start = datetime.strptime(start_str, fmt)
        end = datetime.strptime(end_str, fmt)
        diff = end - start
        
        # Format nice string (e.g., "5m 30s")
        total_seconds = int(diff.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        if minutes > 60:
            hours = minutes // 60
            minutes = minutes % 60
            return f"{hours}h {minutes}m {seconds}s"
        return f"{minutes}m {seconds}s"
    except:
        return "0s"

# --- HEADER ---
st.title("🕵️ Honeypot Agent Command Center")
if st.button("🔄 Refresh Data"):
    st.rerun()

df = load_data()

if not df.empty:
    # --- GLOBAL METRICS ---
    total_scammers = len(df)
    total_msgs = df['msg_count'].sum()
    
    # Calculate Total Time Wasted across ALL sessions
    total_seconds_wasted = 0
    for _, row in df.iterrows():
        try:
            fmt = "%Y-%m-%d %H:%M:%S"
            s = datetime.strptime(row['start_time'], fmt)
            e = datetime.strptime(row['last_update'], fmt)
            total_seconds_wasted += (e - s).total_seconds()
        except: pass
    
    total_min_wasted = int(total_seconds_wasted // 60)
    
    # Global Counters
    all_upis = set()
    for _, row in df.iterrows():
        try:
            d = json.loads(row['extracted_data'])
            all_upis.update(d.get('upiIds', []))
        except: pass

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Sessions", total_scammers)
    c2.metric("Total Messages", total_msgs)
    c3.metric("🔥 UPI IDs Captured", len(all_upis))
    c4.metric("⏳ Total Time Wasted", f"{total_min_wasted} min")

    st.divider()

    # --- MAIN LAYOUT ---
    col_chat, col_intel = st.columns([2, 1.2])

    with col_chat:
        st.subheader("💬 Live Conversation")
        
        # 1. Session Selector
        session_list = df['session_id'].tolist()
        selected_session_id = st.selectbox("Select Active Session:", session_list, index=0)
        
        # Get data for selected session
        session_row = df[df['session_id'] == selected_session_id].iloc[0]
        
        # 2. Render Transcript
        transcript_text = session_row['transcript']
        
        with st.container(height=500, border=True):
            if transcript_text:
                lines = transcript_text.split('\n')
                for line in lines:
                    if not line.strip(): continue
                    
                    if line.startswith("Scammer:"):
                        msg = line.replace("Scammer:", "").strip()
                        with st.chat_message("user", avatar="🤡"):
                            st.write(f"**Scammer:** {msg}")
                            
                    elif line.startswith("Ram Lal:") or line.startswith("Ram Lal"):
                        msg = line.replace("Ram Lal:", "").strip()
                        with st.chat_message("assistant", avatar="👮"):
                            st.write(f"**Ram Lal:** {msg}")
                    else:
                        st.caption(line)
            else:
                st.info("No transcript available.")

    with col_intel:
        # Calculate Specific Session Duration
        duration_str = calculate_duration(session_row['start_time'], session_row['last_update'])
        
        st.subheader(f"🛡️ Intel: {selected_session_id}")
        st.metric("⏱️ Time Wasted (This Scammer)", duration_str)
        
        try:
            intel = json.loads(session_row['extracted_data'])
        except:
            intel = {}

        # UPI
        upis = intel.get('upiIds', [])
        st.info(f"**💰 UPI IDs ({len(upis)})**")
        if upis:
            for item in upis: st.code(item, language="text")
        else:
            st.caption("No UPIs found.")

        # BANKS
        banks = intel.get('bankAccounts', [])
        st.warning(f"**🏦 Bank Accounts ({len(banks)})**")
        if banks:
            for item in banks: st.code(item, language="text")
        else:
            st.caption("No Bank Accounts found.")
            
        # PHONES
        phones = intel.get('phoneNumbers', [])
        st.success(f"**📞 Phone Numbers ({len(phones)})**")
        if phones:
            for item in phones: st.code(item, language="text")
        else:
            st.caption("No Phone Numbers found.")

        # LINKS
        links = intel.get('phishingLinks', [])
        st.error(f"**🔗 Phishing Links ({len(links)})**")
        if links:
            for item in links: st.code(item, language="text")
        else:
            st.caption("No Links found.")

else:
    st.warning("Waiting for the first scammer interaction...")