import logging
import numpy as np
from sentence_transformers import SentenceTransformer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EmbeddingService:
    """
    A service class for generating semantic vector embeddings from text.
    
    Why use this?
    - Text strings cannot be directly compared for "meaning".
    - Embeddings convert text into a high-dimensional mathematical vector (an array of numbers).
    - Sentences with similar meanings will have vectors that point in similar directions in space.
    
    We use the 'all-MiniLM-L6-v2' model because:
    1. It is extremely fast and lightweight.
    2. It produces high-quality sentence embeddings.
    3. It runs well on CPUs (does not require a dedicated GPU).
    """

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the EmbeddingService by loading the pre-trained SentenceTransformer model.
        
        Args:
            model_name (str): The name of the model to load from HuggingFace.
        
        Time Complexity: O(1) after the model is downloaded, but loading from disk takes some I/O time.
        Memory Complexity: O(M) where M is the size of the model weights (MiniLM is ~90MB in RAM).
        """
        logging.info(f"Loading SentenceTransformer model: {model_name}")
        # The model is loaded into memory here. For production, you usually load this ONCE at startup.
        self.model = SentenceTransformer(model_name)
        logging.info("Model loaded successfully.")

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Converts a given text string into a mathematical vector (NumPy array).
        
        How it works internally:
        1. Tokenization: The text is split into sub-words (tokens).
        2. Transformer Layers: Tokens pass through attention mechanisms to understand context.
        3. Pooling: The outputs are averaged to create a single fixed-size vector (384 dimensions for MiniLM).
        
        Args:
            text (str): The text to embed (e.g., Resume text or Job Description).
            
        Returns:
            np.ndarray: A 1D array of 384 float32 numbers representing the text's semantic meaning.
            
        Time Complexity: O(N) where N is the number of tokens in the text.
        Memory Complexity: O(N) for storing the intermediate activations during inference.
        """
        if not text or not text.strip():
            logging.warning("Empty text provided for embedding. Returning zero vector.")
            # MiniLM produces 384-dimensional embeddings. We return a zero vector for empty strings.
            return np.zeros(384, dtype=np.float32)
            
        # encode() returns a numpy array representing the embedding
        return self.model.encode(text)
