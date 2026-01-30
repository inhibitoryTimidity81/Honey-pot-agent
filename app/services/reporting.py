import requests
from app.core.config import settings

def send_final_callback(session_id: str, analysis_result: dict):
    """
    Sends the mandatory final report to GUVI.
    We call this as a Background Task so it doesn't slow down the chat.
    """
    
    # 1. Unpack the analysis data from Member 3's code
    intel = analysis_result.get("intelligence", {})
    metrics = analysis_result.get("metrics", {})
    extracted = intel.get("extracted_data", {})

    # 2. Construct the Payload (Exact format from PDF Page 9)
    payload = {
        "sessionId": session_id,
        "scamDetected": intel.get("is_scam", True),
        "totalMessagesExchanged": metrics.get("totalMessagesExchanged", 0),
        "extractedIntelligence": {
            "bankAccounts": extracted.get("bankAccounts", []),
            "upiIds": extracted.get("upiIds", []),
            "phishingLinks": extracted.get("phishingLinks", []),
            "phoneNumbers": extracted.get("phoneNumbers", []),
            # Add any other fields if your regex finds them
        },
        "agentNotes": intel.get("agent_notes", "Automated report from Ram Lal Agent.")
    }

    # 3. Send to GUVI
    try:
        # We use a timeout so your server doesn't hang if theirs is slow
        response = requests.post(
            settings.GUVI_CALLBACK_URL, 
            json=payload, 
            timeout=5
        )
        if response.status_code == 200:
            print(f"✅ Report SENT for {session_id}")
        else:
            print(f"⚠️ Report REJECTED for {session_id}: {response.text}")
            
    except Exception as e:
        print(f"❌ Report FAILED for {session_id}: {e}")