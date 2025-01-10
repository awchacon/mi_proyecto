from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
import os
import streamlit as st
import gc
from types import AppState

embeddings = OllamaEmbeddings(model="llama3.1")

# Funciones auxiliares (sin cambios importantes, salvo la carga en Chroma)
def cargar_documentos_en_chroma(articulos, state: AppState):
    persist_directory = "./chroma_db"
    try:
        if articulos:
            documentos = [Document(page_content=articulo["resumen"], metadata={"titulo": articulo["titulo"], "enlace": articulo["enlace"]}) for articulo in articulos]
            if state["vector_store"] is None:
                state["vector_store"] = Chroma.from_documents(documentos, embeddings, persist_directory=persist_directory)
                st.success(f"{len(documentos)} documentos cargados en ChromaDB (creación nueva).")
            else:
                state["vector_store"].add_documents(documentos) #Añadir los nuevos documentos
                state["vector_store"].persist()
                st.success(f"{len(documentos)} documentos añadidos a ChromaDB.")
        else:
            st.warning("No hay documentos para cargar en ChromaDB.")
    except Exception as e:
        st.error(f"Error al cargar/crear ChromaDB: {e}")
        state["vector_store"] = None
