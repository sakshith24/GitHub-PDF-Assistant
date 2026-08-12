import chromadb
from sentence_transformers import SentenceTransformer

def retrieve_query(query):
    chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
    collection = chroma_client.get_collection(name = "github-pdf-collection")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    query_embedding = model.encode(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )
    return results
    # with open("./data/chroma_db" ,'r') as file:
