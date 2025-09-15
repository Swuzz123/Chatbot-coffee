from utils.query_utils import is_exact_item
from retrieval.milvus_search import general_search_and_recommend, search_exact_item

def handle_user_query(query, limit=5):
    # Case 1: Check exact item
    is_exact, exact_item = is_exact_item(query)
    if is_exact:
        results = search_exact_item(query)
        if results:
            return results
    
    # Case 2: General recommend
    return general_search_and_recommend(query, limit)
    