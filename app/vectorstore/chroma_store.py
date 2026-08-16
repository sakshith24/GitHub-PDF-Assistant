import chromadb
# from langchain_core.documents import Document

def collection_pdf_github(chunks,embeddings,source_type,source_name):
    chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
    collection = chroma_client.get_or_create_collection(name = "github-pdf-collection")
    ids = [
        f"{source_type}_{source_name}_{i}"
        for i in range(len(chunks))
    ]
    metadata = []
    for chunk in chunks:
        meta = chunk.metadata.copy()
        meta["type"] = source_type
        meta["source_name"] = source_name
        metadata.append(meta)
    documents = [chunk.page_content for chunk in chunks]
    collection.upsert(
        ids=ids,
        documents= documents,
        metadatas=metadata,
        embeddings=embeddings
    )
    return collection
