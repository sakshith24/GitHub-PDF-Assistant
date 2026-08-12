import chromadb
from langchain_core.documents import Document

def collection_pdf_github(chunks,embeddings):
    chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
    collection = chroma_client.get_or_create_collection(name = "github-pdf-collection")
    ids = [f"chunks_{i}" for i in range(len(chunks))]
    metadata = [chunk.metadata for chunk in chunks]
    document = [chunk.page_content for chunk in chunks]
    collection.add(
        ids=ids,
        documents= document,
        metadatas=metadata,
        embeddings=embeddings
    )
    return collection
