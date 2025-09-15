import os
from dotenv import load_dotenv
from huggingface_hub import login
from pymilvus import connections, Collection
from embedding_model.core import EmbeddingModel
from sentence_transformers import CrossEncoder
from utils.query_utils import is_exact_item, get_category_from_query
from config.settings import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME, mappings

# Load .env file
load_dotenv()
login(os.getenv("HF_TOKEN"))

# Connect to Milvus
connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
collection = Collection(COLLECTION_NAME)
collection.load()
print(f"Loaded sucessfully collection {COLLECTION_NAME}")

model = EmbeddingModel()
rerank_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Case 1: If the customer directly asks to buy that item, then respond accurately.
def search_exact_item(query):
    is_exact, exact_title = is_exact_item(query)
    if not is_exact:
        return None, None
    
    expr = f'Title == "{exact_title}"'
    
    try:
        search_results = collection.search(
            data = [model.get_embedding(exact_title)],
            anns_field="embedding",
            param={"metric_type": "L2", "params": {"nprobe": 8}},
            limit=1,
            expr=expr,
            output_fields=["Title", "Price", "Description", "Image_url"]
        )
    except Exception as e:
        print(f"Error search: {e}")
        return None, None
    
    retrieval_results = [
        {
            "title": hit.entity.get("Title"),
            "description": hit.entity.get("Description"),
            "price": hit.entity.get("Price"),
            "image_url": hit.entity.get("Image_url"),
        }
        for hit in search_results[0]
    ]
    return retrieval_results

# Case 2: When the user asks a general question about a type of beverage/food
def general_search_and_recommend(query, limit):
    query_embedding = model.get_embedding(query)
    
    main_cat, sub_cat = get_category_from_query(model.preprocess_text(query))
    
    expr = f''
    if main_cat and sub_cat:
        expr += f'Main_category == "{main_cat}" and Sub_category == "{sub_cat}"'
    elif main_cat:
        # If have no sub_category in query
        if sub_cat is None:
            sub_list = list(mappings[main_cat].keys())
            
            # If have more than 1 sub_category, return list of sub_category
            if len(sub_list) > 1: 
                if len(sub_list) == 2:
                    final_ans = f"{sub_list[0]} và {sub_list[1]}"
                else:
                    final_ans = ", ".join(sub_list[:-1]) + f" và {sub_list[-1]}"
                return f"Quán mình có các loại {main_cat.lower()} như: {final_ans}"
            
            # If just have 1 sub_category or empty, recommend base on that directly
            else:
                expr = f'Main_category == "{main_cat}"'
                
    try:
        search_results = collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param={"metric_type": "L2", "params": {"nprobe": 8}},
            limit=limit,
            expr=expr,
            output_fields=["Title", "Price", "Description", "Image_url"]
        )
    except Exception as e:
        print(f"Search error: {e}")
        return None, None
    
    # Parse retrieval results
    retrieval_results = [
        {
            "title": hit.entity.get("Title"),
            "description": hit.entity.get("Description"),
            "price": hit.entity.get("Price"),
            "image_url": hit.entity.get("Image_url"),
        }
        for hit in search_results[0]
    ]
    
    # Rarank with Cross-Encoder
    if retrieval_results:
        pairs = [(query, f"{r['title']} {r['description']}") for r in retrieval_results]
        scores = rerank_model.predict(pairs)
        reranked_results = sorted(zip(retrieval_results, scores), key=lambda x: x[1], reverse=True)
    else: 
        return None
    
    # Return final retrieval
    final_retrieval = [r for r, s in reranked_results if r in retrieval_results][:limit]
    return final_retrieval 