import os
import re
import pandas as pd
import pyodbc
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility

# Load file .env
load_dotenv()

# ================ Connect SQL Server ================
server = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")

conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)
print(f"Connection string: {conn_str}")

# Load data from SQL Server
try:
    conn = pyodbc.connect(conn_str)
    query = "SELECT * FROM products"
    data = pd.read_sql(query, conn)
    conn.close()
except Exception as e:
    print("Error connecting to SQL Server: {e}")
    exit(1)
    
print("Data colums:", data.columns.tolist())
print(data.head())

# Preprocess text function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    text = re.sub(r"\d+", "", text)      # Remove numbers
    text = re.sub(r"\s+", " ", text)     # Remove extra spaces
    return text.strip()

# Embed texts
data["combined_text"] = data.apply(
    lambda row: preprocess_text(f"{row['Title']} {row['Description']}"),
    axis=1
)

# Create embedding function
def embed_texts(texts, batch_size=50):
    embed_model = SentenceTransformer("keepitreal/vietnamese-sbert")
    # Preprocess text
    texts = [preprocess_text(text) for text in texts]
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = embed_model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
        embeddings.extend(batch_embeddings)
    return embeddings

# Set the collection name and dimension for the embeddings
COLLECTION_NAME = "coffee_embeddings"
DIMENSION = 768

# ================ Connect to Milvus server (Docker) ================
try: 
    connections.connect(host="localhost", port="19530")
except Exception as e:
    print(f"Error connecting to Milvus: {e}")
    exit(1)
    
# Delete collection if it's existed
if utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)
    
# ================ Create collection which includes the information about the coffee menu ================

# 1. Define structured collection
fields = [
    FieldSchema(name="ProductID", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="Title", dtype=DataType.VARCHAR, max_length=255),
    FieldSchema(name="Price", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="Image_url", dtype=DataType.VARCHAR, max_length=2000),
    FieldSchema(name="Description", dtype=DataType.VARCHAR, max_length=2000),
    FieldSchema(name="Main_category", dtype=DataType.VARCHAR, max_length=255),
    FieldSchema(name="Sub_category", dtype=DataType.VARCHAR, max_length=255),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
]

# 2. Add fields to schema
schema = CollectionSchema(fields=fields, description="Coffee menu")
collection = Collection(name=COLLECTION_NAME, schema=schema)

# ================ Insert data (no batch) ================
try:
    embeddings = embed_texts(data['combined_text'].tolist(), batch_size=50)
    entities = [
        {
            "ProductID": int(row["ProductID"]),
            "Title": row["Title"] or "",
            "Price": row["Price"] or "",
            "Image_url": row["Image_url"] or "",
            "Description": row["Description"] or "",
            "Main_category": row["Main_category"] or "",
            "Sub_category": row["Sub_category"] or "",
            "embedding": emb
        }
        for row, emb in zip(data.to_dict('records'), embeddings)
    ]
    
    collection.insert(entities)
    collection.flush()              # sysnc data into database
    print(f"Inserted {len(entities)} entities into Milvus")
except Exception as e:
    print(f"Error inserting data into Milvus: {e}")
    exit(1)

# ================ Create index and load collection ================
try:
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 16}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    collection.load()
    print(f"Created index and loaded collection")
except Exception as e:
    print(f"Error creating index or loading collection: {e}")
    exit(1)
    
# Check the number of entities
try:
    print(f"Total entities in Milvus: {collection.num_entities}")
except Exception as e:
    print(f"Error querying Milvus: {e}")
    exit(1)