import numpy as np

def cosine_similarity(vector1: np.ndarray, vector2: np.ndarray):
    """
    Calcula la similitud coseno entre dos vectores
    """
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
