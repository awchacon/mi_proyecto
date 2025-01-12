from typing import List, TypedDict
import streamlit as st
from utils.arxiv import search_in_arxiv, process_xml_arxiv
from vector_db.chroma_db import load_documents_in_chrome
from app_state import AppState


def search_agent(state: AppState, root_dir: str):
    consulta = state["consulta"]
    xml_data = search_in_arxiv(consulta)
    mensajes = state.get("mensajes", [])

    if xml_data:
        articulos = process_xml_arxiv(xml_data)
        state["articulos"] = articulos
        mensajes.append({"role": "system", "content": f"Se encontraron {len(articulos)} artículos."})

        
        load_documents_in_chrome(articulos, state, root_dir)

        st.session_state.app_state = state  # Actualizar el estado 
    else:
        mensajes.append({"role": "system", "content": "No se encontraron artículos en ArXiv."})
        state["articulos"] = []

    state["mensajes"] = mensajes
    if "resumenes_aprobados" not in state:
        state["resumenes_aprobados"] = {}
    st.session_state.app_state = state #Actualizar el estado
    return state