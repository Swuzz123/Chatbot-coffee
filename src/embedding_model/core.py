import re
from sentence_transformers import SentenceTransformer

class EmbeddingModel():
    def __init__(self):
        self.embedding_model = SentenceTransformer("keepitreal/vietnamese-sbert")
    
    # Preprocess text function
    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
        text = re.sub(r"\d+", "", text)      # Remove numbers
        text = re.sub(r"\s+", " ", text)     # Remove extra spaces
        return text.strip()
    
    # Embedding function 
    def get_embedding(self, text):
        if not text.strip():
            return []
        
        text = self.preprocess_text(text)
        embedding = self.embedding_model.encode(text, convert_to_numpy=True, show_progress_bar=False)
        return embedding