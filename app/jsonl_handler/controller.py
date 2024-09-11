import json
import logging as log

def read_jsonl(file_path: str) -> list:
    """
    Lee un archivo json y devuelve todos los articulos encontrados en él.
    """
    valid_data = []
    with open(file_path, 'r') as input_file:
        for line_number, line_content in enumerate(input_file):
            try:
                line_object = json.loads(line_content) 
                # Type validation, si el objeto no contiene type será omitido
                if 'type' in line_object and line_object['type'] != 'article': 
                    continue
                
                # Columns validation
                if not all(key in line_object for key in ['type', 'text', 'url']):
                    log.warning(f"Linea {line_number+1} omitida por estructura de artículo inválida")
                    continue
                
                valid_data.append(line_object)
            except ValueError:
                log.warning(f"Linea {line_number+1} omitida por no estar en formato json")
                continue

    return valid_data
    


def write_jsonl(jsons_list: list,file_path) -> bool:
    """
    Escribe una lista de diccionarios como json en un archivo.
    """
    with open(file_path,'w') as output:
        for obj in jsons_list:
            output.write(json.dumps(obj) + '\n')
    return True