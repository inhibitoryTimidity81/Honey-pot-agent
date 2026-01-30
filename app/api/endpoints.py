from fastapi import APIRouter, Header, HTTPException, BackgroundTasks
from app.models.schemas import IncomingRequest, APIResponse
from app.services import gemini_agent, intelligence, reporting
from app.core.config import settings

router = APIRouter()

@router.post("/chat", response_model=APIResponse)
@router.post("/chat", response_model=APIResponse)
async def chat_endpoint(
    payload: IncomingRequest, 
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(None)
):
    # Security ...
    if x_api_key != settings.YOUR_SECRET_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # --- PRINT INCOMING MESSAGE ---
    print(f"\n[🔴 SCAMMER]: {payload.message.text}")

    # Analyze & Reply ...
    intel_data = intelligence.analyze_session(payload.sessionId, payload.conversationHistory, payload.message.text)
    ai_reply = gemini_agent.generate_response(payload.conversationHistory, payload.message.text)

    # --- PRINT OUTGOING MESSAGE ---
    print(f"[🟢 RAM LAL]: {ai_reply}")
    print(f"[🔍 INTEL]: Found {len(intel_data['intelligence']['extracted_data']['upiIds'])} UPI IDs")

    # Report ...
    background_tasks.add_task(reporting.send_final_callback, payload.sessionId, intel_data)

    # ... (rest of the code above remains the same) ...

    # --- 5. RETURN RESPONSE (Fixed) ---
    # We must match the schema exactly.
    return {
        "status": "success",
        "scamDetected": True,
        "responseMessage": ai_reply,
        
        # The Schema demands these fields, so we map them from our intel_data
        "agentNotes": intel_data["intelligence"].get("agent_notes", "Engaging scammer..."),
        
        "extractedIntelligence": intel_data["intelligence"].get("extracted_data", {
            "bankAccounts": [], "upiIds": [], "phoneNumbers": [], "phishingLinks": []
        }),
        
        "engagementMetrics": {
            "totalMessagesExchanged": intel_data["metrics"]["totalMessagesExchanged"],
            "engagementDurationSeconds": intel_data["metrics"]["engagementDurationSeconds"]
        }
    }