import json
import chromadb
import google.generativeai as genai
from llm.tools import calculate_total_price
from llm.system_prompt import get_relevant_chunk, make_prompt
from embedding_model.core import EmbeddingModel
from config.settings import GEMINI_API_KEY, CHROMA_COLLECTION_NAME, SIMILARITY_THRESHOLD, system_prompt_content

class CoffeeChatbot:
    def __init__(self):
        # Initialize Gemini API
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Initialize tools for LLM
        self.tools = [
            genai.protos.Tool(
                function_declarations=[
                    genai.protos.FunctionDeclaration(
                        name='calculate_total_price',
                        description='Calculates the total price of all items ordered in the conservation.',
                        parameters=genai.protos.Schema(
                            type=genai.protos.Type.OBJECT,
                            properties={} # No parameters needed as it uses chat history
                        ),
                    ),
                ]
            )    
        ]
        # Initialize the generative model with the tools
        self.model = genai.GenerativeModel('gemini-1.5-flash', tools=self.tools)
        
        # Initialize embedding model
        self.embedding_model = EmbeddingModel()
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path='D:/Workspace/RAG/Chatbot coffee/src/coffee_chat_db') 
        self.collection = self.chroma_client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"} # Using cosine similarity
        )
        
        
    def generate_embedding(self, text):
        """"Create embedding for text with EmbeddingModel"""
        
        embedding = self.embedding_model.get_embedding(text)
        if embedding is None:
            return []
        
        return embedding.tolist()
        
    def generate_answer_from_llm(self, query, chat_history, context_data):
        """"Generate answer from Gemini API with function calling support"""
        
        # Limit chat history
        if len(chat_history) > 50:
            chat_history[:] = chat_history[-50:]  # Short-term memmory
            
        # Format chat history for Gemini API
        gemini_history = []
        for entry in chat_history:
            if entry.startswith("User:"):
                gemini_history.append({'role': 'user', 'parts': [{'text': entry.replace("User:", "", 1).strip()}]})
            elif entry.startswith("Assistant:"):
                gemini_history.append({'role': 'model', 'parts': [{'text': entry.replace("Assistant:", "", 1).strip()}]})
                
        # Determine the full prompt to send to the model
        if "tổng tiền" in query.lower() or "tính tiền" in query.lower():
            # For calculation queries, a simple prompt is sufficient
            # The model will decide whether to call the function based on the query and tool description.
            prompt = query
        else:
            # For regular queries, use the RAG context
            prompt = make_prompt(query, context_data['context'])
        
        try:
            # First call: Ask the model to generate content or a function call
            response = self.model.generate_content(
                gemini_history + [
                    {'role': 'user', 'parts': [{'text': prompt}]}
                ]
            )
            
            # Check if the model has requested to call a function
            if response.candidates and 'function_call' in response.candidates[0].content.parts[0]:
                function_call = response.candidates[0].content.parts[0].function_call
                
                # Execute the function if it's 'calculate_total_price'
                if function_call.name == "calculate_total_price":
                    # Call the actual Python function with the chat history
                    result_json_str = calculate_total_price(chat_history, context_data)
                    
                    # Second call: Send the function's result back to the model
                    # This allows the model to generate a final, human-readable answer.
                    response = self.model.generate_content(
                        gemini_history + [
                            {'role': 'user', 'parts': [{'text': prompt}]},
                            {'role': 'model', 'parts': [response.candidates[0].content.parts[0]]},
                            {'role': 'function', 'name': 'calculate_total_price', 'parts': [{'text': result_json_str}]}
                        ]
                    )

            answer = response.text if response.text else "Không nhận được câu trả lời từ mô hình."
            return answer
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Mình xin lỗi vì gặp chút trục trặc. Bạn có thể hỏi lại hoặc thử món khác nhé!"
    
    def generate_answer(self, query, chat_history):
        """
        Main function to handle chat queries.
        It manages the caching logic and calls the LLM for new answers.
        """
        
        # Step 1: Check if the user's intent is to calculate the total price
        is_calculation_query = "tổng tiền" in query.lower() or "tính tiền" in query.lower()
        
        if is_calculation_query:
            response = self.generate_answer_from_llm(query, chat_history, {'context': None, 'image_url': []})
            return response, []
        
        # Step 2: Retrieve relevant context from Milvus and/or ChromaDB
        context_data = get_relevant_chunk(query)
        context = context_data.get("context", "Không tìm thấy được thông tin món trong database")
        image_url = context_data.get("image_url", [])
        
        images_data = []
        if context and image_url:
            try:
                item_contexts = context.split("---")
                for i, item_context in enumerate(item_contexts):
                    if item_context.strip() and i < len(image_url):
                        title = ""
                        for line in item_context.strip().split("\n"):
                            if line.startswith("Tên:"):
                                title = line.replace("Tên:", "").strip()
                                break
                        # Gắn tên món và URL vào một dictionary
                        if title:
                            images_data.append({"name": title, "image_url": image_url[i]})
            except Exception as e:
                print(f"Lỗi khi xử lý context để tạo images_data: {e}")
                images_data = []
        
        # Step 3: Embed the query for ChromaDB
        query_embedding = self.generate_embedding(query)
        
        if not query_embedding:
            response = self.generate_answer_from_llm(query, chat_history, context_data)
            return response, images_data
            
        # Step 4: Search for a similar query in the cache
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        
        if results['distances'] and len(results['distances'][0]) > 0 and results['distances'][0][0] <= (1 - SIMILARITY_THRESHOLD):
            cached_metadata = results['metadatas'][0][0]
            cached_response = cached_metadata['response']
            cached_image_url_str = cached_metadata.get("image_url")
            
            try:
                cached_image_url = json.loads(cached_image_url_str)
            except (json.JSONDecodeError, TypeError):
                cached_image_url = []

            print(f"Using cached response for query: {query}")
            return cached_response, cached_image_url
            
        # Step 5: If no cache hit, generate a new answer
        response = self.generate_answer_from_llm(query, chat_history, context_data)
        
        if response == "Mình xin lỗi vì gặp chút trục trặc. Bạn có thể hỏi lại hoặc thử món khác nhé!":
            return response, images_data
        
        # Store new answer in the cache
        self.collection.add(
            embeddings=[query_embedding],
            documents=[query],
            metadatas=[{"query": query, "response": response, "context": context, "image_url": json.dumps(images_data)}],
            ids=[str(hash(query))]
        )
        print(f"Generated and cached new response for query: {query}")
        
        return response, images_data
