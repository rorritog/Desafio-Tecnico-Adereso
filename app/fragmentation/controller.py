from app.configs import FRAGMENTS_MAX_TOKENS
import urllib.parse
import tiktoken

tokenizer = tiktoken.encoding_for_model("gpt-4")

def fragmentize_article(article: dict) -> dict:
    """
    Fragmenta un articulo y devuelve la data procesada 
    """
    # Extraer la información relevante de la url:
    parsed_url = urllib.parse.urlparse(article['url'])
    relevant_url_information = parsed_url.path.split('/')[1::2]
    clean_relevant_tokens = [urllib.parse.unquote(subpart).replace('-',' ') for subpart in relevant_url_information]
    
    # Procesamiento del contenido y división en fragmentos
    raw_sub_fragments = [urllib.parse.unquote(subpart) for subpart in article['text'].split('. ')]

    fragments = []
    current_fragment = ""
    current_fragment_counter = 0
    for sub_fragment in raw_sub_fragments:
        sub_fragment_tokens = len(tokenizer.encode(sub_fragment))
        if current_fragment_counter + sub_fragment_tokens <= FRAGMENTS_MAX_TOKENS:
            current_fragment += f"{sub_fragment}. "
            current_fragment_counter += sub_fragment_tokens
        else:
            fragments.append(current_fragment)
            current_fragment_counter = sub_fragment_tokens
            current_fragment = sub_fragment
    fragments.append(current_fragment)

    # Devolver data procesada
    return {
        'url': article['url'],
        'content': urllib.parse.unquote(article['text']),
        'url_relevant_tokens': clean_relevant_tokens,
        'fragments': fragments,
    }
