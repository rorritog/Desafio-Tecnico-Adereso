from app.jsonl_handler.controller import read_jsonl, write_jsonl
import os

def test_json_handling() -> None:
    """
    Prueba el correcto funcionamiento de las funciones de lectura y escritura de archivos jsonl
    """
    json_lines = [
        {
            "type": "article", 
            "url": "https://www.sample.url/some-endpoint", 
            "text": "Valid Row"
        },
        {
            "type": "article", 
            "url": "https://www.sample.url/some-endpoint", 
            "text": "Valid Row 2",
            "valid": True
        },
        {
            "type": "not article", 
            "url": "https://www.sample.url/some-endpoint", 
            "text": "Invalid 1"
        },
        {
            "valid": False, 
            "text": "Invalid 2"
        },
    ]
    # Escribir jsonl
    tmp_filename = 'tmp_test_json_handling.jsonl'
    write_jsonl(json_lines, tmp_filename)

    # Leer rows
    valid_articles = read_jsonl(tmp_filename)

    # Eliminar archivo
    os.remove(tmp_filename)
    
    expected_articles_text = ["Valid Row","Valid Row 2"]
    assert [article['text'] for article in valid_articles] == expected_articles_text