from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.docstore.document import Document
import os

embeddings = OllamaEmbeddings(model="llama3.1")

def load_documents_in_chroma(articulos, state, root_dir):
    persist_directory = os.path.join(root_dir, "chroma_db")
    if state["vector_store"] is None:
        state["vector_store"] = Chroma.from_documents(client=None, documents=[], embedding_function=embeddings.embed_query, persist_directory=persist_directory)
    if articulos:
        documentos_para_chroma = []
        for articulo in articulos:
            documentos_para_chroma.append(
                Document(page_content=articulo["titulo"] + " " + articulo.get("abstract", ""),
                         metadata={"titulo": articulo["titulo"], "enlace": articulo["enlace"], "publicado": articulo["publicado"]})
            )
        state["vector_store"].add_documents(documents=documentos_para_chroma)
        state["vector_store"].persist()