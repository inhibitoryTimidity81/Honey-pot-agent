import google.generativeai as genai
import json
import re
import time
from typing import List
from app.core.config import settings
from app.models.schemas import MessageContent

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

# In-Memory Stats
SESSION_STATS = {}

SYSTEM_PROMPT = """
You are a Cybersecurity Intelligence Analyst. 
Analyze the CONVERSATION HISTORY and the LATEST MESSAGE.

YOUR TASKS:
1. SCAM DETECTION: Determine if this is a scam (True/False).
2. SUMMARIZATION: Write a brief "Agent Note" summarizing the scammer's persona.
3. EXTRACTION: Extract details like UPI, bank details, phone numbers, and links.

OUTPUT FORMAT (Raw JSON):
{
    "is_scam": boolean,
    "agent_notes": "string summary",
    "extracted_data": {
        "bankAccounts": [],
        "upiIds": [],
        "phoneNumbers": [],
        "phishingLinks": []
    }
}
"""

def extract_via_regex(text: str) -> dict:
    """
    Fallback function to extract patterns when AI fails.
    """
    # 1. UPI IDs (e.g., something@okicici, number@paytm)
    upi_pattern = r"[\w\.\-_]+@[\w]+"
    
    # 2. Indian Phone Numbers (10 digits starting with 6-9, optional +91)
    phone_pattern = r"(?:\+91[\-\s]?)?[6-9]\d{9}\b"
    
    # 3. Phishing Links (http/https)
    link_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+\S*"
    
    # 4. Bank Account Numbers (Simple check: 9 to 18 digits in a row)
    # Note: This might pick up random long numbers, but better safe than sorry in a fallback.
    bank_pattern = r"\b\d{9,18}\b"

    return {
        "bankAccounts": list(set(re.findall(bank_pattern, text))),
        "upiIds": list(set(re.findall(upi_pattern, text))),
        "phoneNumbers": list(set(re.findall(phone_pattern, text))),
        "phishingLinks": list(set(re.findall(link_pattern, text)))
    }

def analyze_session(session_id: str, history: List[MessageContent], current_text: str) -> dict:
    
    # --- 1. Update Metrics ---
    current_time = time.time()
    if session_id not in SESSION_STATS:
        SESSION_STATS[session_id] = {"msg_count": 0, "start_time": current_time}
    
    stats = SESSION_STATS[session_id]
    stats["msg_count"] += 1
    duration = int(current_time - stats["start_time"])

    # --- 2. Format History ---
    transcript = ""
    for msg in history:
        transcript += f"{msg.sender}: {msg.text}\n"
    transcript += f"Scammer: {current_text}"

    # --- 3. Intelligence Extraction ---
    try:
        # A. Try AI Extraction First
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nTRANSCRIPT:\n{transcript}")
        clean_text = response.text.strip().replace("```json", "").replace("```", "")
        ai_data = json.loads(clean_text)
        
    except Exception as e:
        # B. Fallback to Regex if AI fails
        print(f"⚠️ AI Intelligence Failed: {e}. Switching to Regex Fallback.")
        
        # Run regex on the FULL transcript to catch details shared earlier
        regex_data = extract_via_regex(transcript)
        
        ai_data = {
            "is_scam": True, # Default to True in a Honeypot scenario
            "agent_notes": f"AI unavailable. Data extracted via Regex. Error: {str(e)}",
            "extracted_data": regex_data
        }

    return {
        "intelligence": ai_data,
        "metrics": {
            "totalMessagesExchanged": stats["msg_count"],
            "engagementDurationSeconds": duration
        }
    }