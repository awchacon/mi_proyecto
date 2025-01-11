import streamlit as st
from langgraph.graph import StateGraph
from typing import List, TypedDict
import time
from langchain.vectorstores import Chroma
import tweepy
from agents.search import buscar_agente
from utils.twitter import publicar_en_twitter_v2, client
from agents.summarize import resumir_agente
from vector_db.chroma_db import embeddings #Importar embeddings
from app_state import AppState
import os
from langchain.chains import RetrievalQA
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama


# Inicialización del modelo de Ollama y embeddings (FUERA DE CUALQUIER FUNCIÓN)
try:
    llm = Ollama(model="llama3.1", temperature=0.1)
    embeddings = OllamaEmbeddings(model="llama3.1")
except Exception as e:
    st.error(f"Error al inicializar Ollama: {e}")
    st.stop()

# Inicialización del estado de Streamlit (AL INICIO DEL SCRIPT)
if "app_state" not in st.session_state:
    st.session_state.app_state = AppState(consulta="", articulos=[], resumenes={}, resumenes_aprobados={}, mensajes=[], vector_store=None)

app_state = st.session_state.app_state

# Inicialización de Chroma (FUERA DE LAS PESTAÑAS Y DENTRO DE UN IF)
if app_state["vector_store"] is None:
    persist_directory = "chroma_db"  # Ruta a tu base de datos Chroma
    try:
        app_state["vector_store"] = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        st.info("ChromaDB cargado correctamente.")
    except Exception as e:
        st.error(f"Error al cargar ChromaDB: {e}. Asegúrate de que existe la carpeta chroma_db y que contiene datos. Error: {e}")
        app_state["vector_store"] = None
        st.stop() #Detener la ejecucion si hay un error en la carga de chromadb
st.session_state.app_state = app_state


# PESTAÑAS
tab1, tab2 = st.tabs(["Búsqueda y Publicación", "Chat con ChromaDB"])



# Pestaña 1: Búsqueda y Publicación (Código que ya tenías, con las correcciones anteriores)
with tab1:
        # Interfaz de Streamlit
    st.title("ArXiv to X Agent System")

    # Inicialización de Chroma (DESPUÉS de inicializar app_state)
    root_dir = os.getcwd()
    persist_directory = os.path.join(root_dir, "chroma_db")
    if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 0:
        try:
            app_state["vector_store"] = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
            st.info("ChromaDB cargado desde disco.")
        except Exception as e:
            st.error(f"Error al cargar ChromaDB desde disco: {e}")
            app_state["vector_store"] = None
    else:
        st.info("No se encontró una base de datos Chroma existente. Se creará una nueva al buscar artículos.")
        app_state["vector_store"] = None

    st.session_state.app_state = app_state # Actualizar el estado en session_state

    # Grafo de LangGraph
    graph_builder = StateGraph(AppState)
    graph_builder.add_node("buscar", lambda state: buscar_agente(state, root_dir))
    graph_builder.add_node("resumir", resumir_agente)
    #graph_builder.add_node("publicar", publicar_agente) #No se usa directamente
    graph_builder.set_entry_point("buscar")
    graph_builder.add_edge("buscar", "resumir")
    #graph_builder.add_edge("resumir", "publicar") #No se usa directamente
    graph = graph_builder.compile()

    # Interacción con el usuario en Streamlit
    consulta = st.text_input("Introduce tu consulta en ArXiv:")

    if st.button("Buscar en ArXiv"):
        with st.spinner("Buscando publicaciones..."):
            app_state["consulta"] = consulta
            app_state = graph.invoke(app_state)
            st.session_state.app_state = app_state

    # Mostrar artículos y generar/aprobar resúmenes
    if app_state["articulos"]:
        for i, articulo in enumerate(app_state["articulos"]):
            st.subheader(f"Artículo {i+1}")
            st.text(f"Título: {articulo['titulo']}")
            st.text(f"Publicado: {articulo['publicado']}")
            st.markdown(f"[Enlace al artículo]({articulo['enlace']})")

            if i not in app_state["resumenes"]:
                if st.button(f"Resumir artículo {i+1}"):
                    with st.spinner("Generando resumen..."):
                        app_state = graph.invoke(app_state)
                        st.session_state.app_state = app_state
            else:
                st.success("Resumen existente:")
                st.write(app_state["resumenes"][i])

            if i in app_state["resumenes"]:
                nuevo_resumen = st.text_area(f"Edita el resumen (artículo {i+1}):", app_state["resumenes"][i])
                if st.button(f"Aprobar resumen {i+1}"):
                    app_state["resumenes_aprobados"][i] = nuevo_resumen
                    st.session_state.app_state = app_state
                    st.success("Resumen aprobado y guardado.")

    # Sección de Publicar en X (Twitter)
    if st.session_state.app_state["resumenes_aprobados"]:
        st.markdown("## Publicar en X (Twitter)")
        for i, resumen in st.session_state.app_state["resumenes_aprobados"].items():
            st.write(f"**Artículo {i+1}:** {resumen}")
            if client:
                if st.button(f"Publicar artículo {i+1} en X"):
                    with st.spinner("Publicando en X..."):
                        try:
                            resumen_str = str(resumen)
                            resultado = publicar_en_twitter_v2(resumen_str)
                            st.session_state.app_state = app_state
                            if "Publicado en X con éxito" in resultado:
                                st.success(resultado)
                            else:
                                st.error(resultado)
                            time.sleep(5)
                        except tweepy.TooManyRequests as e:
                            st.error(f"Error al publicar en Twitter: Demasiadas solicitudes. Espera un momento. Detalles: {e}")
                            time.sleep(60)
                        except Exception as e:
                            st.error(f"Error al publicar en Twitter: {str(e)}")
            else:
                st.warning("No se pudo publicar en Twitter debido a un error de autenticación")

    # Buscar en Chroma
    pregunta = st.text_input("Haz tu pregunta sobre los artículos cargados:")
    if st.button("Buscar en Chroma"):
        try:
            if app_state["vector_store"]:
                with st.spinner("Buscando en Chroma..."):
                    resultados = app_state["vector_store"].similarity_search(pregunta, k=3)

                    if resultados:
                        st.write("Resultados:")
                        for i, resultado in enumerate(resultados):
                            with st.expander(f"Resultado {i+1}: {resultado.metadata.get('titulo', 'Sin título')}"):
                                st.markdown(f"**Contenido:** {resultado.page_content}")
                                st.markdown(f"**Metadatos:** {resultado.metadata}")
                    else:
                        st.info("No se encontraron resultados para tu búsqueda.")

            else:
                st.warning("ChromaDB no está inicializado. Busca y carga artículos primero.")
        except Exception as e:
            st.error(f"Error al buscar en ChromaDB: {str(e)}")

    # Mostrar mensajes del sistema
    st.write("Mensajes del sistema:")
    for mensaje in app_state["mensajes"]:
        st.write(f"- {mensaje['content']}")

# Pestaña 2: Chat con ChromaDB
with tab2:
    st.title("Chat con ChromaDB")
    user_question = st.text_input("Pregunta:")

    if st.button("Enviar"):
        if user_question:
            if app_state["vector_store"]: #Comprobar si chromadb se ha inicializado
                try:
                    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=app_state["vector_store"].as_retriever())
                    with st.spinner("Pensando..."):
                        result = qa({"query": user_question})
                    st.write("Respuesta:", result["result"])
                except Exception as e:
                    st.error(f"Error al procesar la pregunta: {e}")
            else:
                st.warning("ChromaDB no está inicializado. Busca y carga artículos primero en la otra pestaña.")