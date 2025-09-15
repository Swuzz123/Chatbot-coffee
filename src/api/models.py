from pydantic import BaseModel
from typing import List

# Receive query from user and store in chat_history
class ChatRequest(BaseModel):
    query: str 
    chat_history: List[str] = []
    
# Return reponse for user and update chat_history
class ChatResponse(BaseModel):
    response: str 
    chat_history: List[str]    
    image_urls: List[str] = None