from abc import ABC, abstractmethod
from typing import List, Any

class EmbeddingProvider(ABC):
    @abstractmethod
    def generate(self, text: str) -> Any:
        """Generates embeddings for the given text."""
        pass
