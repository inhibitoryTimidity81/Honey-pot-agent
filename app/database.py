import sqlite3
import json
from datetime import datetime

DB_NAME = "honeypot_logs.db"

def init_db():
    """Creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            start_time TEXT,
            last_update TEXT,
            msg_count INTEGER,
            is_scam BOOLEAN,
            extracted_data TEXT,
            transcript TEXT
        )
    ''')
    conn.commit()
    conn.close()

def update_session(session_id, msg_count, is_scam, extracted_data, transcript):
    """Upserts (Update or Insert) session data."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Convert dicts/lists to JSON strings for storage
    extracted_json = json.dumps(extracted_data)
    
    # Check if exists
    c.execute("SELECT session_id FROM sessions WHERE session_id = ?", (session_id,))
    exists = c.fetchone()
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if exists:
        c.execute('''
            UPDATE sessions 
            SET last_update = ?, msg_count = ?, is_scam = ?, extracted_data = ?, transcript = ?
            WHERE session_id = ?
        ''', (now, msg_count, is_scam, extracted_json, transcript, session_id))
    else:
        c.execute('''
            INSERT INTO sessions (session_id, start_time, last_update, msg_count, is_scam, extracted_data, transcript)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, now, now, msg_count, is_scam, extracted_json, transcript))
        
    conn.commit()
    conn.close()