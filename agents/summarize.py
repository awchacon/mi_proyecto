from typing import List, TypedDict
import streamlit as st
from utils.llm import generate_summary_adjusted
from app_state import AppState

def summarize_agent(state: AppState):
    articulos = state["articulos"]
    resumenes = {}
    mensajes = state.get("mensajes", [])
    if articulos:
        for i, articulo in enumerate(articulos):
            resumen = generate_summary_adjusted(articulo)
            resumenes[i] = resumen
        mensajes.append({"role": "system", "content": "Resúmenes generados."})
    else:
        mensajes.append({"role": "system", "content": "No hay artículos para resumir."})
    state["resumenes"] = resumenes
    state["mensajes"] = mensajes

    if "resumenes_aprobados" not in state: #Comprobacion simplificada
        state["resumenes_aprobados"] = {}
    return state