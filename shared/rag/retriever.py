from typing import List, Dict
from .store import VectorStore

class Retriever:
    """Retrieves context and builds the prompt augmentation string."""
    def __init__(self, store: VectorStore):
        self.store = store
        
    def retrieve_context(self, query: str) -> str:
        results = self.store.similarity_search(query)
        
        if not results:
            return ""
            
        context_str = "--- Reference Knowledge ---\n"
        for res in results:
            context_str += f"Source ({res['source']}):\n{res['text']}\n\n"
        return context_str
