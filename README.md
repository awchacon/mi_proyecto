# ArXiv & X Agents

Este proyecto implementa un sistema de agentes basado en LangChain para buscar artículos científicos en ArXiv, generar resúmenes y publicarlos en X (anteriormente Twitter).

## Explicación

Este proyecto demuestra la creación de un prototipo con varios agentes que interactúan para extraer publicaciones científicas de ArXiv y publicarlas en X. Se utiliza LangGraph para orquestar el flujo de trabajo entre los agentes, ChromaDB para el almacenamiento de embeddings y Ollama como LLM.

## Requisitos

*   Python 3.10+
*   Dependencias listadas en `requirements.txt` (ver sección Instalación)
*   Cuenta de desarrollador en X (Twitter) con las credenciales configuradas.
*   Instancia de Ollama corriendo con el modelo `llama3.1` disponible.


1.  Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

1.  Ejecuta la aplicación Streamlit:

    ```bash
    streamlit run app.py
    ```

2.  Abre la aplicación en tu navegador (la URL se mostrará en la terminal).

3.  En la pestaña "Búsqueda y Publicación", introduce una consulta en ArXiv y haz clic en "Buscar en ArXiv".

4.  Revisa los artículos encontrados, genera resúmenes y apruébalos.

5.  En la pestaña "Chat con ChromaDB", puedes hacer preguntas sobre los artículos que has cargado.

## Estructura del proyecto

MI_PROYECTO/
*   agents/
    *   publish.py
    *   search.py
    *   summarize.py
*   chroma_db/
    *   ...
*   utils/
    *   arxiv.py
    *   llm.py
    *   twitter.py
*   vector_db/
    *   chroma_db.py
*   .gitignore
*   app_state.py
*   app.py
*   README.md

## Dependencias

*   `langchain`
*   `langchain-community`
*   `langchain-ollama`
*   `streamlit`
*   `arxiv`
*   `tweepy`
*   Otras dependencias (ver `requirements.txt`)

## Próximas mejoras

*   Implementación de reranking con Cohere.
*   Mejoras en la interfaz de usuario.
*   Manejo de errores más robusto.
*   Implementación de un sistema de feedback más sofisticado.
*   Soporte para otras plataformas además de X (Twitter).
