from app.condensation.controller import embedding_model
from app.condensation.vector_operations import cosine_similarity


def test_cosine_similarity() -> None:
    """
    Prueba si el paradigma de la similitud coseno es efectiva
    """

    text1 = "I enjoy hiking in the mountains during the weekends."
    text2 = "On weekends, I love going for a hike in the hills."

    embedding1 = embedding_model.encode(text1)
    embedding2 = embedding_model.encode(text2)

    # Check si la función cosine_similarity detecta similaridad mayor a 0.85 entre las dos oraciones
    assert cosine_similarity(embedding1,embedding2) > 0.85