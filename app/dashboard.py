import streamlit as st
import pandas as pd
import json
import sqlite3
import time

# --- CONFIG ---
st.set_page_config(page_title="Honeypot Live Intel", layout="wide")
DB_NAME = "honeypot_logs.db"

# --- FUNCTIONS ---
def load_data():
    """Reads from the SQLite DB created by FastAPI"""
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_NAME)
        # Read the table into a Pandas DataFrame
        df = pd.read_sql_query("SELECT * FROM sessions", conn)
        conn.close()
        return df
    except Exception:
        # If DB doesn't exist yet (no scams caught), return empty
        return pd.DataFrame()

# --- HEADER ---
st.title("🕵️ Honeypot Agent Command Center")
st.markdown("Live monitoring of scam interactions and intelligence extraction.")

# Auto-refresh button (Streamlit re-runs the script when clicked)
if st.button("🔄 Refresh Data"):
    st.rerun()

# --- METRICS ROW ---
df = load_data()

if not df.empty:
    # 1. Calculate Summary Metrics
    total_scammers = len(df)
    total_msgs = df['msg_count'].sum()
    
    # 2. Extract all UPIs and Banks into lists
    all_upis = []
    all_banks = []
    
    # Loop through every row to dig out the JSON data
    for index, row in df.iterrows():
        try:
            # The data is stored as a string, so we convert it back to JSON
            data = json.loads(row['extracted_data'])
            
            # Add found items to our master lists
            all_upis.extend(data.get('upiIds', []))
            all_banks.extend(data.get('bankAccounts', []))
        except:
            pass # Skip if data is corrupted or empty

    # 3. Display Metrics at the top
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Sessions", total_scammers)
    col2.metric("Total Messages", total_msgs)
    col3.metric("🔥 UPI IDs Captured", len(set(all_upis)))       # set() removes duplicates
    col4.metric("🏦 Bank Accts Captured", len(set(all_banks)))

    st.divider()

    # --- TWO COLUMNS: CHAT LOGS & INTEL ---
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("🔴 Live Engagement Logs")
        
        # Show a clean table of sessions (hiding the long transcript)
        display_df = df[['session_id', 'last_update', 'msg_count', 'is_scam']].copy()
        st.dataframe(display_df, use_container_width=True)
        
        # Dropdown to select a specific scammer
        st.write("---")
        selected_session = st.selectbox("Select Session to View Transcript", df['session_id'].unique())
        
        if selected_session:
            # Find the row that matches the selected ID
            session_row = df[df['session_id'] == selected_session].iloc[0]
            # Show the transcript in a scrollable text box
            st.text_area("Full Transcript", session_row['transcript'], height=400)

    with c2:
        st.subheader("🛡️ Extracted Intelligence")
        
        st.write("### 💰 UPI IDs")
        if all_upis:
            # Show unique UPIs
            st.code("\n".join(set(all_upis)), language="text")
        else:
            st.info("No UPIs captured yet.")

        st.write("### 🏦 Bank Accounts")
        if all_banks:
            # Show unique Bank Accounts
            st.code("\n".join(set(all_banks)), language="text")
        else:
            st.info("No Accounts captured yet.")

else:
    # What to show if the database is empty
    st.warning("Waiting for the backend to log the first session...")
    st.info("💡 Tip: Send a message to your API to see data appear here.")