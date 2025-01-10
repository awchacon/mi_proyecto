import streamlit as st
from langgraph.graph import StateGraph
from typing import List, TypedDict
from types import AppState #Importar AppState desde types.py
import time
from langchain.vectorstores import Chroma
import tweepy
from agents.search import buscar_agente
from utils.twitter import publicar_en_twitter_v2, client
from agents.summarize import resumir_agente

# Definir el estado del grafo
class AppState(TypedDict):
    consulta: str
    articulos: List[dict]
    resumenes: dict
    resumenes_aprobados: dict
    mensajes: List[dict]
    vector_store: Chroma

# Interfaz de Streamlit
st.title("ArXiv to X Agent System")

# Inicialización del estado en Streamlit
if "app_state" not in st.session_state:
    st.session_state.app_state = AppState(consulta="", articulos=[], resumenes={}, resumenes_aprobados={}, mensajes=[], vector_store=None)

app_state = st.session_state.app_state

st.session_state.app_state = app_state # Actualizar el estado

# Grafo de LangGraph
graph_builder = StateGraph(AppState)
graph_builder.add_node("buscar", buscar_agente)
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