from app.configs import FILE_INPUT_PATH, FILE_OUTPUT_PATH
from app.condensation.controller import generate_article_fragments, assign_fragments_references
from app.fragmentation.controller import fragmentize_article
from app.jsonl_handler.controller import read_jsonl, write_jsonl
import logging as log

def main():
    # leer el archivo de entrada
    log.info(f"Leyendo el archivo de entrada: {FILE_INPUT_PATH}")
    input_articles = read_jsonl(FILE_INPUT_PATH)
    log.info(f"Total de articulos leidos: {len(input_articles)}")

    # procesar articulos
    output_fragments = []
    already_generated_tag = set()
    log.info(f"Procesando articulos")
    for index, article in enumerate(input_articles):
        article['alredy_generated_tasks'] = list(already_generated_tag)

        log.info(f"Fragmentando articulo {index+1}")
        fragmented_article = fragmentize_article(article)
        log.info(f"procesando articulo {index+1}")
        processed_fragments = generate_article_fragments(fragmented_article)

        # Agregar tags ya generados a arreglo de control
        for fragment in processed_fragments:
            already_generated_tag.update(fragment['tags'])

        output_fragments +=  assign_fragments_references(processed_fragments)
    # Escribir el resultado
    log.info(f"Escribiendo archivo de salida: {FILE_OUTPUT_PATH}")
    write_jsonl(output_fragments,FILE_OUTPUT_PATH)

    log.info(f"Script finalizado. Fragmentos obtenidos: {len(output_fragments)}")

if __name__ == '__main__':
    main()
