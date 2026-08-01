import os
from typing import List, Dict

class DocumentLoader:
    """Loads markdown or text documents from a directory."""
    def __init__(self, directory: str = "knowledge"):
        self.directory = directory
        
    def load_all(self) -> List[Dict[str, str]]:
        documents = []
        if not os.path.exists(self.directory):
            return documents
            
        for filename in os.listdir(self.directory):
            if filename.endswith(".md") or filename.endswith(".txt"):
                filepath = os.path.join(self.directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append({"source": filename, "content": content})
        return documents
