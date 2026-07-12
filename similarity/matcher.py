import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SemanticMatcher:
    """
    A class responsible for determining the semantic similarity between vectors.
    
    Why Cosine Similarity?
    - If two vectors point in the same direction, the angle between them is 0, and cosine(0) = 1 (100% match).
    - If they are completely unrelated (orthogonal), the angle is 90, and cosine(90) = 0 (0% match).
    - Unlike Euclidean distance, Cosine Similarity cares about the *direction* (meaning), not the magnitude (length of text).
    """

    @staticmethod
    def calculate_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculates the Cosine Similarity between two 1D NumPy arrays (embeddings).
        
        Args:
            vec1 (np.ndarray): The first embedding vector (e.g., Resume).
            vec2 (np.ndarray): The second embedding vector (e.g., Job Description).
            
        Returns:
            float: A similarity score between 0.0 and 1.0.
            
        Time Complexity: O(D) where D is the dimensionality of the embeddings (384 for MiniLM).
        Memory Complexity: O(1) beyond the memory used to hold the two vectors.
        """
        # Ensure vectors are not entirely zeros (which would cause a divide-by-zero warning in cosine calculation)
        if not np.any(vec1) or not np.any(vec2):
            logging.warning("One or both vectors are empty/zeros. Similarity is 0.0.")
            return 0.0
            
        # Reshape 1D arrays to 2D arrays expected by sklearn (1 sample, D features)
        v1 = vec1.reshape(1, -1)
        v2 = vec2.reshape(1, -1)
        
        # Calculate cosine similarity. Returns a 2D array [[score]]
        similarity_matrix = cosine_similarity(v1, v2)
        score = similarity_matrix[0][0]
        
        # Clip to ensure floating point errors don't push it slightly outside [0, 1] bounds
        score = float(np.clip(score, 0.0, 1.0))
        return score
