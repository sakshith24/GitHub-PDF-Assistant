import chromadb
from sentence_transformers import SentenceTransformer

def retrieve_query(query,n_results,source):
    chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
    collection = chroma_client.get_collection(name = "github-pdf-collection")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    query_embedding = model.encode(query)
    source = source.lower()

    # -------------------------
    # PDF ONLY
    # -------------------------
    if source == "pdf":

        return collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"type": "pdf"},
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

    # -------------------------
    # GITHUB ONLY
    # -------------------------
    elif source == "github":

        return collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"type": "github"},
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

    # -------------------------
    # ALL
    # -------------------------
    elif source == "all":

        pdf_results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"type": "pdf"},
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        github_results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"type": "github"},
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        combined = []

        for i in range(len(pdf_results["documents"][0])):
            combined.append({
                "document": pdf_results["documents"][0][i],
                "metadata": pdf_results["metadatas"][0][i],
                "distance": pdf_results["distances"][0][i],
            })

        for i in range(len(github_results["documents"][0])):
            combined.append({
                "document": github_results["documents"][0][i],
                "metadata": github_results["metadatas"][0][i],
                "distance": github_results["distances"][0][i],
            })

        # Smaller distance = more similar
        combined.sort(key=lambda x: x["distance"])

        combined = combined[:n_results]

        return {
            "documents": [
                [item["document"] for item in combined]
            ],
            "metadatas": [
                [item["metadata"] for item in combined]
            ],
            "distances": [
                [item["distance"] for item in combined]
            ],
        }

    else:
        raise ValueError(
            f"Invalid source: {source}"
        )




    # query_args = {
    #     "query_embeddings": [query_embedding],
    #     "n_results": n_results,
    #     "include" :["documents", "metadatas", "distances"]
    # }

    # if source == "PDF":
    #     query_args["where"] = {
    #         "type": "pdf"
    #     }
    # elif source =="github":
    #     query_args["where"]={
    #         "type": "github"
    #     }
    # results = collection.query(**query_args)
    # return results
    # with open("./data/chroma_db" ,'r') as file:
