from typing import List, TypedDict
import streamlit as st
from utils.twitter import publicar_en_twitter_v2
from types import AppState

def publicar_agente(state: AppState):
    mensajes = state.get("mensajes", [])
    if not state["resumenes_aprobados"]:
        mensajes.append({"role": "system", "content": "No hay resúmenes para publicar."})
        state["mensajes"] = mensajes
        return state

    for i, resumen in enumerate(state["resumenes_aprobados"]): # Usar enumerate aquí
        try:
            resultado_publicacion = publicar_en_twitter_v2(resumen)
            mensajes.append({"role": "system", "content": f"Publicado resumen {i+1}: {resultado_publicacion}"})
        except Exception as e:
            mensajes.append({"role": "system", "content": f"Error al publicar resumen {i+1}: {e}"})
    state["mensajes"] = mensajes

    if "resumenes_aprobados" not in state: #Comprobacion simplificada
        state["resumenes_aprobados"] = {}
    return state