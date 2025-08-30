import google.generativeai as genai
from config.settings import GEMINI_API_KEY, system_prompt_content
from llm.system_prompt import get_relevant_chunk, make_prompt

def generate_answer(query, chat_history, limit=5):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Take context from get_relevant_chunk
    context = get_relevant_chunk(query)
    
    # Create prompt
    prompt = make_prompt(query, context)
    
    # Apppend the prompt to chat history
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]
    chat_history.append(f'User: {prompt}')
    
    # Combine system message to chat history
    full_prompt = f"{system_prompt_content}\n\n" + "\n".join(chat_history) + f"\n\n{prompt}\nAssistant:"
    
    # Generate response
    try:
        response = model.generate_content(full_prompt)
        chat_history.append(f"Assistant: {response.text}")
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Mình xin lỗi vì gặp chút trục trặc. Bạn có thể hỏi lại hoặc thử món khác nhé!"