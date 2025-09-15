from fastapi import FastAPI, HTTPException
from api.models import ChatRequest, ChatResponse
from llm.generate import CoffeeChatbot

app = FastAPI(title="Coffee Chatbot AI", description="API for Coffee Chatbot", version="1.0.0")

# Initialize the CoffeeChatbot instance
coffee_bot = CoffeeChatbot()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response, images_data = coffee_bot.generate_answer(request.query, request.chat_history)
        if response is None:
            raise HTTPException(status_code=500, detail="Không thể tạo câu trả lời")
        
        return ChatResponse(
            response=response,
            chat_history=request.chat_history,
            image_url=images_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Request bị lỗi {str(e)}")