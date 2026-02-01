# from fastapi import APIRouter, Header, HTTPException, BackgroundTasks
# from app.models.schemas import IncomingRequest, APIResponse
# from app.services import gemini_agent, intelligence, reporting
# from app.core.config import settings

# router = APIRouter()

# @router.post("/chat", response_model=APIResponse)
# @router.post("/chat", response_model=APIResponse)
# async def chat_endpoint(
#     payload: IncomingRequest, 
#     background_tasks: BackgroundTasks,
#     x_api_key: str = Header(None)
# ):
#     # Security ...
#     if x_api_key != settings.YOUR_SECRET_API_KEY:
#         raise HTTPException(status_code=401, detail="Invalid API Key")

#     # --- PRINT INCOMING MESSAGE ---
#     print(f"\n[🔴 SCAMMER]: {payload.message.text}")

#     # Analyze & Reply ...
#     intel_data = intelligence.analyze_session(payload.sessionId, payload.conversationHistory, payload.message.text)
#     ai_reply = gemini_agent.generate_response(payload.conversationHistory, payload.message.text)

#     # --- PRINT OUTGOING MESSAGE ---
#     print(f"[🟢 RAM LAL]: {ai_reply}")
#     print(f"[🔍 INTEL]: Found {len(intel_data['intelligence']['extracted_data']['upiIds'])} UPI IDs")

#     # Report ...
#     background_tasks.add_task(reporting.send_final_callback, payload.sessionId, intel_data)

#     # ... (rest of the code above remains the same) ...

#     # --- 5. RETURN RESPONSE (Fixed) ---
#     # We must match the schema exactly.
#     return {
#         "status": "success",
#         "scamDetected": True,
#         "responseMessage": ai_reply,
        
#         # The Schema demands these fields, so we map them from our intel_data
#         "agentNotes": intel_data["intelligence"].get("agent_notes", "Engaging scammer..."),
        
#         "extractedIntelligence": intel_data["intelligence"].get("extracted_data", {
#             "bankAccounts": [], "upiIds": [], "phoneNumbers": [], "phishingLinks": []
#         }),
        
#         "engagementMetrics": {
#             "totalMessagesExchanged": intel_data["metrics"]["totalMessagesExchanged"],
#             "engagementDurationSeconds": intel_data["metrics"]["engagementDurationSeconds"]
#         }
#     }

from fastapi import APIRouter, Header, HTTPException, BackgroundTasks
from app.models.schemas import IncomingRequest, APIResponse
from app.services import gemini_agent, intelligence, reporting
from app.core.config import settings
from app import database  # <--- IMPORTED DATABASE

router = APIRouter()

@router.post("/chat", response_model=APIResponse)
async def chat_endpoint(
    payload: IncomingRequest, 
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(None)
):
    # Security Check
    if x_api_key != settings.YOUR_SECRET_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # --- PRINT INCOMING MESSAGE ---
    print(f"\n[🔴 SCAMMER]: {payload.message.text}")

    # 1. Analyze & Extract Intel (This does the first DB Save)
    intel_data = intelligence.analyze_session(payload.sessionId, payload.conversationHistory, payload.message.text)
    
    # 2. Generate Ram Lal's Reply
    ai_reply = gemini_agent.generate_response(payload.conversationHistory, payload.message.text)

    # --- PRINT OUTGOING MESSAGE ---
    print(f"[🟢 RAM LAL]: {ai_reply}")
    print(f"[🔍 INTEL]: Found {len(intel_data['intelligence']['extracted_data']['upiIds'])} UPI IDs")

    # 3. Report to GUVI
    background_tasks.add_task(reporting.send_final_callback, payload.sessionId, intel_data)

    # --- 4. CRITICAL FIX: SAVE FULL TRANSCRIPT TO DB ---
    # We reconstruct the full chat including Ram Lal's new reply so the Dashboard sees it.
    
    full_transcript = ""
    # Add history
    for msg in payload.conversationHistory:
        full_transcript += f"{msg.sender}: {msg.text}\n"
    # Add current exchange
    full_transcript += f"Scammer: {payload.message.text}\n"
    full_transcript += f"Ram Lal: {ai_reply}"

    try:
        database.update_session(
            session_id=payload.sessionId,
            msg_count=intel_data["metrics"]["totalMessagesExchanged"],
            is_scam=intel_data["intelligence"].get("is_scam", True),
            extracted_data=intel_data["intelligence"].get("extracted_data", {}),
            transcript=full_transcript # <--- Saving the COMPLETE chat
        )
    except Exception as e:
        print(f"⚠️ Secondary DB Save Error: {e}")

    # 5. Return Response
    return {
        "status": "success",
        "scamDetected": True,
        "responseMessage": ai_reply,
        "agentNotes": intel_data["intelligence"].get("agent_notes", "Engaging scammer..."),
        "extractedIntelligence": intel_data["intelligence"].get("extracted_data", {
            "bankAccounts": [], "upiIds": [], "phoneNumbers": [], "phishingLinks": []
        }),
        "engagementMetrics": {
            "totalMessagesExchanged": intel_data["metrics"]["totalMessagesExchanged"],
            "engagementDurationSeconds": intel_data["metrics"]["engagementDurationSeconds"]
        }
    }