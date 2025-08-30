import os
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer, CrossEncoder
from huggingface_hub import login
from config.settings import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME, mappings, sub_category_keywords
from embedding_model.core import EmbeddingModel
from dotenv import load_dotenv

# Load .env file
load_dotenv()
login(os.getenv("HF_TOKEN"))

# Connect to Milvus
connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
collection = Collection(COLLECTION_NAME)
collection.load()
print(f"Loaded sucessfully collection {COLLECTION_NAME}")

# Case 1: If the customer directly asks to buy that item, then respond accurately.
def is_exact_item(query):
    query = query.strip().lower()
    for main_cat, sub_cats in mappings.items():
        for sub_cat, items in sub_cats.items():
            for item in items:
                if item.lower() in query:
                    return True, item     
    return False, None

def search_exact_item(query):
    is_exact, exact_title = is_exact_item(query)
    if not is_exact:
        return None, None
    
    expr = f'Title == {exact_title}'
    
    try:
        search_results = collection.search(
            data = [EmbeddingModel.get_embedding(exact_title)],
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
def get_category_from_query(query):
    query =  query.lower()
    
    # 1. Check suggested keywords for sub_category
    for main_cat, sub_cats in mappings.items():
        for sub_cat in sub_cats.keys():
            if sub_cat:
                if sub_cat in sub_category_keywords:
                    for keywords in sub_category_keywords[sub_cat]:
                        if keywords in query:
                            return main_cat, sub_cat
                        
    # 2. Check directly sub_category
    for main_cat, sub_cats in mappings.items():
        for sub_cat in sub_cats.keys():
            if sub_cat and sub_cat.lower() in query:
                return main_cat, sub_cat
            
    # 3. Check directly main_category
    for main_cat in mappings.keys():
        if main_cat.lower() in query:
            return main_cat, None
        
    # 4. Check keywords by each items (fallback)
    for main_cat, sub_cats in mappings.items():
        for sub_cat, items in sub_cats.items():
            for item in items:
                if item.lower() in query:
                    return main_cat, sub_cat
                
    return None, None

def general_search_and_recommend(query, limit):
    model = EmbeddingModel()
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
    rerank_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    if retrieval_results:
        pairs = [(query, f"{r['title']} {r['description']}") for r in retrieval_results]
        scores = rerank_model.predict(pairs)
        reranked_results = sorted(zip(retrieval_results, scores), key=lambda x: x[1], reverse=True)
    else: 
        return None
    
    # Return final retrieval
    final_retrieval = [r for r, s in reranked_results if r in retrieval_results][:limit]
    return final_retrieval 