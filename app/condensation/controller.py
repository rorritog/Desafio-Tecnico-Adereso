
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from app.configs import COSINE_SIMILARITY_THRESHOLD, OPENAI_LLM_MODEL, OPENAI_LLM_TEMPERATURE, TRANSFORMERS_EMBEDING_MODEL
from app.condensation.prompts import get_system_prompt, generate_user_prompt
from app.condensation.vector_operations import cosine_similarity
from uuid import uuid1

import json

# Open AI client para la fragmentación de articulos
openai_client = OpenAI()
# Transformers model para la transformacion de strings a vectores
embedding_model = SentenceTransformer(TRANSFORMERS_EMBEDING_MODEL)


def generate_article_fragments(article: dict) -> list:
    """
    Consulta a la api de openAI para generar los fragmentos de un artículo
    """
    user_prompt = generate_user_prompt(article)
    system_prompt = get_system_prompt()
    completion = openai_client.chat.completions.create(
        model=OPENAI_LLM_MODEL,
        temperature=OPENAI_LLM_TEMPERATURE,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"}
    )

    return json.loads((completion.choices[0].message.content))['fragments']

def assign_fragments_references(fragments: list) -> list:
    """
    Asigna referencias tipo uuid a un conjunto de fragmentos
    """
    fragments_with_references = fragments.copy()
    generated_uuids = [uuid1().hex for _ in fragments_with_references]
    # Asignar uuid y related_fragments a cada fragmento
    for fragment, fragment_uuid in zip(fragments_with_references, generated_uuids):
        fragment['uuid'] = fragment_uuid
        fragment['related_fragments'] = [uuid for uuid in generated_uuids if uuid != fragment_uuid]

    return fragments_with_references


def assign_cross_fragments_references(fragments: list) -> list:
    """
    Asigna referencias cruzadas entre distintos fragmentos a través del calculo de la similitud coseno entre los resumenes.
    """
    fragments_with_cross_references = fragments.copy()

    # Vectorización de cada resumen de fragmentos
    embeddings = {}
    for fragment in fragments_with_cross_references:
        embeddings[fragment['uuid']] = embedding_model.encode(fragment['summary'])

    # Cálculo de la similitud entre resúmenes
    for fragment in fragments_with_cross_references:
        for related_fragment_uuid, related_fragment_embedding in embeddings.items():
            # Saltar fragmentos ya relacionados
            if related_fragment_uuid == fragment['uuid'] or related_fragment_uuid in fragment['related_fragments']:
                continue

            fragment_embedding = embeddings[fragment['uuid']]
            if cosine_similarity(fragment_embedding, related_fragment_embedding) >= COSINE_SIMILARITY_THRESHOLD:
                fragment['related_fragments'].append(related_fragment_uuid)

    return fragments_with_cross_references