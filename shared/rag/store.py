from typing import List, Dict
import json

class VectorStore:
    """Mock VectorStore wrapping pgvector/local embeddings for the portfolio."""
    def __init__(self, embedding_provider):
        self.provider = embedding_provider
        self.index: List[Dict] = []
        
    def ingest(self, chunks: List[Dict[str, str]]):
        """Generates embeddings and stores them."""
        for chunk in chunks:
            # Generate embedding
            vector = self.provider.generate_embedding(chunk["text"])
            self.index.append({
                "text": chunk["text"],
                "source": chunk["source"],
                "vector": vector
            })
            
    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        """Returns the top_k most similar chunks based on cosine similarity."""
        # For this portfolio MVP, we simulate a vector search return.
        # In production, this executes the pgvector SQL query:
        # SELECT text, source FROM knowledge ORDER BY vector <=> query_vector LIMIT top_k;
        query_vector = self.provider.generate_embedding(query)
        
        # Returning all for now to simulate small scale match
        return [{"text": doc["text"], "source": doc["source"]} for doc in self.index[:top_k]]
