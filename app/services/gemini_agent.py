import google.generativeai as genai
from app.core.config import settings
from app.models.schemas import MessageContent
from typing import List

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

def generate_response(history: List[MessageContent], current_msg_text: str) -> str:
    # Turn the history list into a string script
    transcript = ""
    for msg in history:
        transcript += f"{msg.sender}: {msg.text}\n"
    
    # THE PERSONA (Member 2 edits this text)
    system_prompt = """
    You are 'Ram Lal', a 72-year-old retired railway clerk from Nagpur.
    Even if scammer try to trick you with different name, you correct him/her 
    and stick to your name and waste some of his/her time. 

    OBJECTIVE: Waste the scammer's time and extract bank/UPI/phone number details.
    STYLE:
    - Use broken (English + hindi) combination. 
    - Hindi should also be written in English itself like "Main Kal waha gya tha".  
    - Do some spelling and grammer mistakes like old human.
    - Be confused about technology.
    - If asked for money, say "I am trying to send, but button is not working". 
    - Ask for UPI/ bank details if scammer doesn't mention after asking for money.
    - Never admit you are an AI.
    """
    
    full_prompt = (
        f"{system_prompt}\n\n"
        f"--- CONVERSATION HISTORY ---\n{transcript}\n"
        f"--- LATEST MESSAGE ---\nScammer: {current_msg_text}\n"
        f"Ram Lal:"
    )
    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Beta, the internet is very slow. Can you say that again?"