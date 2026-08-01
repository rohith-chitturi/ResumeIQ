from typing import List, Dict

class TextChunker:
    """Splits large documents into semantic chunks."""
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        chunks = []
        for doc in documents:
            content = doc["content"]
            # Simple paragraph split for MVP
            paragraphs = content.split("\n\n")
            for i, p in enumerate(paragraphs):
                if p.strip():
                    chunks.append({
                        "source": doc["source"],
                        "chunk_id": i,
                        "text": p.strip()
                    })
        return chunks
