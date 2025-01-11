from typing import List, TypedDict
import streamlit as st
from utils.arxiv import buscar_en_arxiv, procesar_xml_arxiv
from vector_db.chroma_db import cargar_documentos_en_chroma
from app_state import AppState


def buscar_agente(state: AppState, root_dir: str):
    consulta = state["consulta"]
    xml_data = buscar_en_arxiv(consulta)
    mensajes = state.get("mensajes", [])

    if xml_data:
        articulos = procesar_xml_arxiv(xml_data)
        state["articulos"] = articulos
        mensajes.append({"role": "system", "content": f"Se encontraron {len(articulos)} artículos."})

        # ***CORRECCIÓN CRUCIAL: LLAMAR A LA FUNCIÓN AQUÍ***
        cargar_documentos_en_chroma(articulos, state, root_dir)

        st.session_state.app_state = state  # Actualizar el estado (esto puede ir al final de la función)
    else:
        mensajes.append({"role": "system", "content": "No se encontraron artículos en ArXiv."})
        state["articulos"] = []

    state["mensajes"] = mensajes
    if "resumenes_aprobados" not in state:
        state["resumenes_aprobados"] = {}
    st.session_state.app_state = state #Actualizar el estado
    return state