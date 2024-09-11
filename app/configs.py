
from dotenv import load_dotenv
import os
import sys
import atexit
import logging

def restore_previous_api_key(OPENAI_API_KEY: str) -> None:
    """
    Restaura el valor original de OPENAI_API_KEY
    """
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

def load_env() -> None:
    """
    Carga el archivo .env en el entorno del script
    """
    # Guardar la llave previamente guardada en el sistema operativo si es que existe
    PREV_STORED_OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    if PREV_STORED_OPENAI_API_KEY:
        del os.environ['OPENAI_API_KEY']
    # Carga de variables del archivo .env a el enviroment de la ejecución del programa
    load_dotenv()
    atexit.register(restore_previous_api_key,PREV_STORED_OPENAI_API_KEY)

def start_logging(log_path: str) -> None:
    """
    Configura el logging de la aplicación
    """
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)-6s %(name)-10s %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)),log_path)),
            logging.StreamHandler(sys.stdout),
        ]
    )


# Configuraciones del uso
## Cantidad máxima de tokens aceptada para un fragmento.
FRAGMENTS_MAX_TOKENS = 1000
## Configuraciones de el Modelo LLM a utilizar
OPENAI_LLM_MODEL = 'gpt-4o-mini'
OPENAI_LLM_TEMPERATURE = 0
## Configuraciones de los archivos de entrada y salida
FILE_INPUT_PATH = 'adereso_cda .jsonl'
FILE_OUTPUT_PATH = 'adereso_cda_fragments.jsonl'
## Configuración de logging
LOGGING_PATH = 'app.log'

# Inicializar modulos
start_logging(LOGGING_PATH)
load_env()



