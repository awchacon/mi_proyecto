# types.py
from typing import List, TypedDict
from langchain_community.vectorstores import Chroma

# Definir el estado del grafo
class AppState(TypedDict):
    consulta: str
    articulos: List[dict]
    resumenes: dict
    resumenes_aprobados: dict
    mensajes: List[dict]
    vector_store: Chroma