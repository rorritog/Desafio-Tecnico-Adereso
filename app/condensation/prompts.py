def get_system_prompt() -> str:
    """
    Función para obtener el prompt del systema en las consultas a la api de openAI. Se utiliza un método get para volverlo inmutable
    """
    return """
        You are a data classification assistant for fragments of an article containing the documentation for an IT functionality.
        You are gonna be provided with a number of fragments from an article in this format:
        <fragment_number>:
        <fragment_content>
              
        Based on the fragments in spanish given by the user you are gonna generate an array of json objects where each element corresponds to one fragment given. The number of fragments in the output array must be equal to the number of input fragments.

        Each fragment json must contain the following fields:

        title: An adequate title for the fragment. Base your criteria on describing what can be achieved with the content of the fragment.
        summary: A summary of the fragment based on its content. Avoid explaining what the fragment contains. 
        tags: Array of Tags relevant to the fragment. Use words related with the IT project itself. Avoid using capital letters.
        article_url: the reference url of the article.
        content: the fragment itself.

        Give only a json object with the key 'fragments' containing the array of json structured fragments as an answer.
        Use the exact fragment in the content field.
        The json generated must be a valid json in the rfc 8259 specification.
    """


def generate_user_prompt(article_data):
    """
    Genera el promtp que entrega la información del artículo, los fragmentos y solicita la generación de fragmentos procesados
    """

    prompt_content = f"""
        Here are the fragmentes of an article: \n
    """

    for index,fragment in enumerate(article_data['fragments']):
        prompt_content += f"{index+1}:\n\n{fragment}\n\n"

    # Ajuste según el contenido en la url del artículo.
    prinpal_concept = article_data['url_relevant_tokens'][:1]
    if prinpal_concept:
        prompt_content += f"Adjust the answer to provide useful information about {prinpal_concept[0]}."
    sub_concepts = article_data['url_relevant_tokens'][1:]
    if sub_concepts:
        prompt_content += f"the content of the article is related to this topics: {', '.join(sub_concepts)}"

    prompt_content += f"""
        This fragments in order form the complete article. The article reference url is: {article_data['url']}.
    """

    return prompt_content