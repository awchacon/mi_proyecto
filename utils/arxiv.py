import requests
import xml.etree.ElementTree as ET
import streamlit as st

# Función para buscar en la API de ArXiv
def search_in_arxiv(consulta, max_results=2):
    params = {"search_query": f"all:{consulta}", "start": 0, "max_results": max_results}
    response = requests.get("http://export.arxiv.org/api/query", params=params)
    if response.status_code == 200:
        return response.text
    else:
        st.error("Error al conectar con la API de ArXiv.")
        return None
    
# Función para procesar datos de ArXiv
def process_xml_arxiv(xml_string):
    namespace = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(xml_string)
    articulos = []
    for entry in root.findall(".//atom:entry", namespace):
        titulo = entry.find("atom:title", namespace).text
        resumen = entry.find("atom:summary", namespace).text
        publicado = entry.find("atom:published", namespace).text
        enlace = entry.find("atom:id", namespace).text
        doi = entry.find("arxiv:doi", namespace)
        comentario = entry.find("arxiv:comment", namespace)

        articulo = {
            "titulo": titulo,
            "resumen": resumen,
            "publicado": publicado,
            "enlace": enlace,
            "doi": doi.text if doi is not None else None,
            "comentario": comentario.text if comentario is not None else None
        }
        articulos.append(articulo)
    return articulos