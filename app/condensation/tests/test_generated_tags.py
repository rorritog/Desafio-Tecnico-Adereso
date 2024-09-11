from app.condensation.controller import openai_client, generate_article_fragments
from app.fragmentation.controller import fragmentize_article
from app.configs import OPENAI_LLM_MODEL, OPENAI_LLM_TEMPERATURE


def test_generated_tags() -> None:
    """
        Prueba si los tags generados para los fragmentos corresponden a los tags generados para el artículo completo.
    """

    article = {
        "type": "article",
        "url": "https://adereso.helpkit.so/adereso-studio/7gcst3pjvWGmqqFfDDVKs7/aderesoai/8HTVeT55T2iXBunRfnZvBv", 
        "text": "\u00bfQu\u00e9 es? En Adereso nos adaptamos a la volatilidad del mercado con continua innovaci\u00f3n en la conexi\u00f3n empresa-cliente. Impulsado por la tecnolog\u00eda avanzada de ChatGPT, nuestro sistema de IA permite simplificar y optimizar la gesti\u00f3n de interacciones. Con Adereso.ai brindamos soluciones para los desaf\u00edos como omnicanalidad, conversi\u00f3n y productividad. Ventajas de la Inteligencia Artificial Generativa Proveer atenci\u00f3n 24/7. Mejorar la eficiencia de nuestros agentes. Pre-clasificar para disminuir la carga de trabajo. Proveer atenci\u00f3n personalizada. Asistencia a la venta. Comunicaci\u00f3n proactiva en todo el viaje del cliente. Productos en Adereso y sus Casos de Uso Dentro de nuestra suite, contamos con las siguiente Soluciones Empresariales: Adereso Studio: Automatizaci\u00f3n de CX. Adereso GPT: Asistente GPT con tus datos. Adereso Desk: Centraliza tu comunicaci\u00f3n. Adereso Engage: Env\u00edos masivos por WhatsApp. Adereso Experience: Encuestas post-atenci\u00f3n. Adereso VoC: Analiza el sentimiento. \ud83d\udd0e En caso de que tengas dudas o el problema persista, comun\u00edcate con nosotros v\u00eda chat, al WhatsApp +56944501722 o al email soporte@adere.so.",
    }

    fragmented_article = fragmentize_article(article)
    generated_fragments = generate_article_fragments(fragmented_article)

    generated_tags = []
    for fragment in generated_fragments:
        generated_tags += fragment['tags']

    completion = openai_client.chat.completions.create(
        model=OPENAI_LLM_MODEL,
        temperature=OPENAI_LLM_TEMPERATURE,
        messages=[
            {"role": "system", "content": "You are gonna be asked to find tags in a text. Provide as an answer only the tags in lowercase found in the text separated by comma"},
            {"role": "user", "content": f"provide tags for this text: {article['text']}"},
        ],
    )
    full_text_tags = completion.choices[0].message.content.split(', ')
    # Check de qué tags aparecen en ambos arreglos
    tags_intersection = [tag.lower() for tag in generated_tags if tag.lower() in full_text_tags]    

    # Tags deben parecerse al menos en un 50%
    assert len(tags_intersection) / len(generated_tags) >= 0.50



