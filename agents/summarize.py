from typing import List, TypedDict
import streamlit as st
from utils.llm import generar_resumen_ajustado
from app_state import AppState

def resumir_agente(state: AppState):
    articulos = state["articulos"]
    resumenes = {}
    mensajes = state.get("mensajes", [])
    if articulos:
        for i, articulo in enumerate(articulos):
            resumen = generar_resumen_ajustado(articulo)
            resumenes[i] = resumen
        mensajes.append({"role": "system", "content": "Resúmenes generados."})
    else:
        mensajes.append({"role": "system", "content": "No hay artículos para resumir."})
    state["resumenes"] = resumenes
    state["mensajes"] = mensajes

    if "resumenes_aprobados" not in state: #Comprobacion simplificada
        state["resumenes_aprobados"] = {}
    return state