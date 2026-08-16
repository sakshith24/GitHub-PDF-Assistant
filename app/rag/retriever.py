import chromadb
from sentence_transformers import SentenceTransformer

def retrieve_query(query,n_results,source):
    chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
    collection = chroma_client.get_collection(name = "github-pdf-collection")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    query_embedding = model.encode(query)
    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": n_results,
        "include" :["documents", "metadatas", "distances"]
    }

    if source == "PDF":
        query_args["where"] = {
            "type": "pdf"
        }
    elif source =="Github":
        query_args["where"]={
            "type": "github"
        }
    results = collection.query(**query_args)
    return results
    # with open("./data/chroma_db" ,'r') as file:
