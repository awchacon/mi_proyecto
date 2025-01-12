from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.docstore.document import Document
import os
from langchain.text_splitter import CharacterTextSplitter

embeddings = OllamaEmbeddings(model="llama3.1")

def load_documents_in_chroma(articulos, state, root_dir):
    persist_directory = os.path.join(root_dir, "chroma_db")

    if state["vector_store"] is None:
        state["vector_store"] = Chroma.from_documents(client=None, documents=[], embedding_function=embeddings, persist_directory=persist_directory)

    if articulos:
        documentos_para_chroma = []
        for articulo in articulos:
            # Combinar título y resumen
            combined_content = f"Título: {articulo['titulo']}\nResumen: {articulo.get('resumen', '')}"
            documentos_para_chroma.append(
                Document(page_content=combined_content, metadata={"titulo": articulo["titulo"], "enlace": articulo["enlace"], "publicado": articulo["publicado"]})
            )
        #Dividir los documentos antes de agregarlos a chromadb
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        split_docs = text_splitter.split_documents(documentos_para_chroma)

        state["vector_store"].add_documents(documents=split_docs) #Agregar los documentos divididos
        state["vector_store"].persist()