# agent/utils.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# ================== INITIALIZE LLM MODEL ==================
API_KEY = os.getenv("GOOGLE_API_KEY")

def initModelLLM():
  try:
    model = ChatGoogleGenerativeAI(
      model='gemini-2.0-flash',
      google_api_key=API_KEY
    )
    return model
  except Exception as e:
    print(f"Cannot load model, reason: {e}")
    return None

# ================== PROMPTING ==================
SYSTEMP_PROMPT = """
You are a staff member at MT coffee shop.
- When starting a conversation, greet the customer with a friendly voice
- If the custoerm asks about drinks of the shop, you have to answer with warm voice and give them as much as details of the drink you have
"""

WELCOME_MSG = "Chào mừng bạn đã đến với của hàng MT' Coffee của chúng tôi, không biết tôi có thể giúp gì được cho bạn nhỉ?"