# Prueba Técnica Rodrigo Galleguillos

Prueba técnica para la postulación al cargo de desarrollador full stack en la empresa Adereso.

## Tabla de contenidos

- [Vista General del Proyecto](#vista-general-del-proyecto)
- [Procedimientos](#procedimientos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Pruebas Unitarias](#pruebas-unitarias)

## Vista general del proyecto

Este repositorio completa el desafío técnico para el puesto de desarrollador full stack en Adereso. El desafío consistente en fragmentar y resumir información acerca de las documentaciones para usuarios de Adereso. Se presenta como entrada un archivo jsonl que contiene todos los docs públicos de la empresa y se busca aplicar el procesamiento de datos en los de tipo Artículo.


## Procedimientos
Para llevar a cabo el cometido de este desafío se llevan a cabo tres procedimientos principales. Cada uno de estos prodecimientos está acompañado con su lógica en módulos separados.

| Etapa | Módulo | Descripción |
|---|---|---|
| Procesamiento de Datos | json_handler | Procesamiento de un archivo jsonl de entrada filtrando información y reconociendo patrones relevantes. |
| Fragmentación de Información | fragmentation | Fragmentación de el contenido de cada artículo obtenido del proceso anterior en fragmentos de información mas pequeños y manejables. |
| Utilización de API de OpenAI para condensamiento de fragmentos | condensation | Resumen, condensación y clasificación de cada fragmento utilizando el LLM Gpt-o4-mini de OpenAI. |

## Instalación
Antes de comenzar se deben asegurar los siguientes prerequisitos:

### Prerequisites

Antes de comenzar asegurate de cumplir con los siguientes requisitos:
- Tener insalado [Python](https://python.org/) en su version 3.11 o superior.

### Pasos

1. Clonar el repositorio:
    ```
    git clone https://github.com/rorritog/Desaf-o-Adereso.git
    ```
2. [Opcional] Utilizar un entorno virtual:
    ```
    python -m venv venv
    ./venv/Scripts/activate
    ```

3. Instalar los paquetes requeridos:
    ```
    python -m pip install -r requirements.txt
    ```

4. Configurar las variables de entorno:
    ```
    cp .env.example .env
    ```
    Para mayor información de este paso visitar la sección [Configuración](#configuración).
5. Ejecutar el archivo main.py:
    ```
    python main.py
    ```
    Para mayor información de este paso visitar la sección [Uso](#uso).

## Configuración
### .env
```bash
# Api key de acceso a la api de openAI. Esta llave debe tener permisos para la utilización del modelo gpt-4o-mini, no debe tener excedida la cuota de uso y debe estar en viegencia
OPENAI_API_KEY=
```
### app/configs.py
Aquí puedes configurar las variables relativas a la ejecución del programa. Esta configuración contiene ciertos valores por defecto que pueden ser modificados y al versionarlos serán persistentes con posibles mejoras del código.
```python
# Configuraciones del uso
## Cantidad máxima de tokens aceptada para un fragmento.
FRAGMENTS_MAX_TOKENS = 1000
## Configuraciones del Modelo LLM a utilizar
OPENAI_LLM_MODEL = 'gpt-4o-mini'
OPENAI_LLM_TEMPERATURE = 0
## Configuraciones de los archivos de entrada y salida
FILE_INPUT_PATH = 'adereso_cda .jsonl'
FILE_OUTPUT_PATH = 'adereso_cda_fragments.jsonl'
## Configuración de logging
LOGGING_PATH = 'app.log'
```

## Uso

Para ejecutar la aplicación es necesario ejecutar el archivo ```main.py```. 

La aplicación soporta la configuración de dos parámetros a través de argumentos por línea de comandos.

- `--input | -i`: Path del archivo jsonl de entrada.
- `--output | -o`: Filename del archivo jsonl de salida. 
- `--help | -h`: Muestra un mensaje de ayuda para estos parámetros.

De no ser recibidos los parámetros, la aplicación tomará los valores configurados en `app/configs.py`.

### Ejemplo de ejecución
```
python main.py -i ./adereso_cda.jsonl -o fragmentos_20240911.jsonl
```

## Pruebas Unitarias
La app puede ser sometida a pruebas unitarias definidas en cada módulo a través de la herramienta [pytest](https://docs.pytest.org/en/stable/). Las pruebas unitarias pueden ser corridas con siguiente comando dentro del directorio raiz y en el entorno de ejecución del programa:
```
pytest
```

### Listado de tests

| Módulo | Archivo | Test | Descripción |
|---|---|---|---|
| condensation | test_generated_tags.py | test_generated_tags | Prueba si los tags generados para los fragmentos corresponden a los tags generados para el artículo completo. |
| condensation | test_prompts.py | test_system_prompt | Prueba si el system prompt es consiso, claro y tiene una estructura entendible. |
| condensation | test_prompts.py | test_user_prompt | Prueba si el system prompt generado para un artículo es claro y tiene una estructura entendible. |
| fragmentation | test_fragmentation.py | test_fragmentation | Prueba si la fragmentación es efectiva a el límite de tokens. |
| json_handler | test_json_handling | test_json_handling | Prueba el correcto funcionamiento de las funciones de lectura y escritura de archivos jsonl |
