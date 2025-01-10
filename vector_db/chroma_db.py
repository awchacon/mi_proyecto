from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
import os
import streamlit as st
import gc
from app_state import AppState

embeddings = OllamaEmbeddings(model="llama3.1")


def cargar_documentos_en_chroma(articulos, state: AppState, root_dir: str): #Añadido root_dir
    persist_directory = os.path.join(root_dir, "chroma_db") #Usar root_dir

    try:
        if articulos:
            documentos = [Document(page_content=articulo["resumen"], metadata={"titulo": articulo["titulo"], "enlace": articulo["enlace"]}) for articulo in articulos]
            if state["vector_store"] is None:
                state["vector_store"] = Chroma.from_documents(documentos, embeddings, persist_directory=persist_directory)
                st.success(f"{len(documentos)} documentos cargados en ChromaDB (creación nueva).")
            else:
                state["vector_store"].add_documents(documentos)
                state["vector_store"].persist()
                st.success(f"{len(documentos)} documentos añadidos a ChromaDB.")
        else:
            st.warning("No hay documentos para cargar en ChromaDB.")
    except Exception as e:
        st.error(f"Error al cargar/crear ChromaDB: {e}")
        state["vector_store"] = None



