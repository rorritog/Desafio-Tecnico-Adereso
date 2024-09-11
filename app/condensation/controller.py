
from openai import OpenAI
from app.configs import OPENAI_LLM_MODEL, OPENAI_LLM_TEMPERATURE
from app.condensation.prompts import get_system_prompt, generate_user_prompt
from uuid import uuid1
import json

openai_client = OpenAI()

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