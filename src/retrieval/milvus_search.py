import os
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer, CrossEncoder
from huggingface_hub import login
from config.settings import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME
from retrieval.query_processor import is_exact_item, get_category_from_query
from dotenv import load_dotenv

# Load .env file
load_dotenv()
login(os.getenv("HF_TOKEN"))

# Connect to Milvus
connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
collection = Collection(COLLECTION_NAME)
collection.load()
print(f"Loaded sucessfully collection {COLLECTION_NAME}")

# Case 1: Search the exact item
def search_exact_item(query):
    is_exact, exact_title = is_exact_item(query)
    if not is_exact:
        return None, None
    
    expr = f'Title == {exact_title}'
    
    try:
        search_results = collection.search(
            data = []
        )